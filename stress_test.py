from locust import HttpUser, TaskSet, task, between

class UserBehavior(TaskSet):
    @task(1)
    def load_main_page(self):
        self.client.get("/")

class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    wait_time = between(1, 5)
