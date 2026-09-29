from app.api.v1.integration import router as integration_router
app.include_router(
    integration_router,
    prefix=settings.API_V1_STR
)
feat(member5): register integration router