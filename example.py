from fcaptcha import hCaptcha

solver: hCaptcha = hCaptcha("")

task: str = solver.create_task(
    site_key="227fe119-8d9e-490c-a0f0-5d9f8a41174d",
    host="https://guns.lol",
    proxy=""
)
solved: str = task.get_result()

print(task.task_id, solved)
