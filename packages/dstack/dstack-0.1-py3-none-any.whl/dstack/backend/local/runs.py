from typing import List, Optional

from dstack.backend.local import jobs, logs, run_names, runners
from dstack.core.app import AppHead
from dstack.core.artifact import ArtifactHead
from dstack.core.job import JobHead
from dstack.core.repo import RepoAddress
from dstack.core.run import RunHead, generate_local_run_name_prefix


def create_run(path: str, repo_address: RepoAddress) -> str:
    name = generate_local_run_name_prefix()
    run_name_index = run_names.next_run_name_index(path, name)
    run_name = f"{name}-{run_name_index}"
    return run_name


def _create_run(path: str, job_head: JobHead, include_request_heads: bool) -> RunHead:
    app_heads = (
        list(map(lambda app_name: AppHead(job_head.job_id, app_name), job_head.app_names))
        if job_head.app_names
        else None
    )
    artifact_heads = (
        list(
            map(
                lambda artifact_path: ArtifactHead(job_head.job_id, artifact_path),
                job_head.artifact_paths,
            )
        )
        if job_head.artifact_paths
        else None
    )
    request_heads = None
    if include_request_heads and job_head.status.is_unfinished():
        if request_heads is None:
            request_heads = []
        job = jobs.get_job(path, job_head.repo_address, job_head.job_id)
        request_head = runners.get_request_head(path, job, None)
        request_heads.append(request_head)
    run_head = RunHead(
        job_head.repo_address,
        job_head.run_name,
        job_head.workflow_name,
        job_head.provider_name,
        job_head.local_repo_user_name,
        artifact_heads or None,
        job_head.status,
        job_head.submitted_at,
        job_head.tag_name,
        app_heads,
        request_heads,
    )
    return run_head


def _update_run(path: str, run: RunHead, job_head: JobHead, include_request_heads: bool):
    run.submitted_at = min(run.submitted_at, job_head.submitted_at)
    if job_head.artifact_paths:
        if run.artifact_heads is None:
            run.artifact_heads = []
        run.artifact_heads.extend(
            list(
                map(
                    lambda artifact_path: ArtifactHead(job_head.job_id, artifact_path),
                    job_head.artifact_paths,
                )
            )
        )
    if job_head.app_names:
        if run.app_heads is None:
            run.app_heads = []
        run.app_heads.extend(
            list(
                map(
                    lambda app_name: AppHead(job_head.job_id, app_name),
                    job_head.app_names,
                )
            )
        )
    if job_head.status.is_unfinished():
        run.status = job_head.status
        if include_request_heads:
            if run.request_heads is None:
                run.request_heads = []
            job = jobs.get_job(path, job_head.repo_address, job_head.job_id)
            request_head = runners.get_request_head(path, job, None)
            run.request_heads.append(request_head)


def get_run_heads(
    path: str, job_heads: List[JobHead], include_request_heads: bool
) -> List[RunHead]:
    runs_by_id = {}
    for job_head in job_heads:
        run_id = ",".join([job_head.run_name, job_head.workflow_name or ""])
        if run_id not in runs_by_id:
            runs_by_id[run_id] = _create_run(path, job_head, include_request_heads)
        else:
            run = runs_by_id[run_id]
            _update_run(path, run, job_head, include_request_heads)
    return sorted(list(runs_by_id.values()), key=lambda r: r.submitted_at, reverse=True)
