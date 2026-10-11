from app.api.v1.integration import router as integration_router
app.include_router(
    integration_router,
    prefix=settings.API_V1_STR
)
GET /api/v1/integration/files/{file_id}/complete-report
/api/v1/integration/files/1/complete-report