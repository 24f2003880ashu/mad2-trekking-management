broker_url = "redis://localhost:6379/0"

result_backend = "redis://localhost:6379/0"

task_ignore_result = True

timezone = "Asia/Kolkata"

beat_schedule = {

    "daily-reminder": {

        "task": "tasks.send_daily_reminder",

        "schedule": 60.0

    },

    "monthly-report": {

        "task": "tasks.send_monthly_report",

        "schedule": 120.0

    }

}