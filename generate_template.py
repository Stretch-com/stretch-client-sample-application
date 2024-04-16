import os

from fastapi.templating import Jinja2Templates


class GenerateTemplateUseCase:
    def __init__(self):
        dir_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        self.templates = Jinja2Templates(directory=f"{dir_path}/static")

    def execute(self, filename, content: dict):
        content["base_url"] = (
            f'{os.getenv("STRETCH_API_URL", "http://localhost")}{os.getenv("STRETCH_API_PREFIX",  "/api/v1")}'  # noqa
        )
        return self.templates.TemplateResponse(
            filename,
            content,
        )