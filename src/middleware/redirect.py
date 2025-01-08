from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse, RedirectResponse
from starlette.middleware.base import BaseHTTPMiddleware


class RedirectMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
            if response.status_code == 401:
                raise HTTPException(status_code=401)
            return response
        except HTTPException as exc:
            if exc.status_code == 401:
                return RedirectResponse(url="/login")
            else:
                return JSONResponse({"detail": exc.detail}, status_code=exc.status_code)
