from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from scripts.database import init_db, log_intake, get_intake_history
from scripts.logger import log_message

init_db()

app = FastAPI()

class WaterIntakeRequest(BaseModel):
    user_id: str
    intake_ml: int

@app.post("/log-intake")
async def log_intake_water(request: WaterIntakeRequest):
    try:
        log_intake(request.user_id, request.intake_ml)
        
        from scripts.agent import WaterIntakeAgent
        agent = WaterIntakeAgent()
        daily_total = get_intake_history(request.user_id)[-1]['total_ml'] if get_intake_history(request.user_id) else request.intake_ml
        analysis = agent.analyze_intake(daily_total)
        
        log_message(f"User {request.user_id} logged {request.intake_ml}ml of water. Total: {daily_total}ml")
        return {"message": "Intake logged successfully", "daily_total_ml": daily_total, "analysis": analysis}
    except Exception as e:
        log_message(f"Error processing intake: {str(e)}", "ERROR")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/intake-history/{user_id}")
def get_intake_history_endpoint(user_id: str):
    try:
        history = get_intake_history(user_id)
        return {'user_id': user_id, "intake_history": history}
    except Exception as e:
        log_message(f"Error fetching history for {user_id}: {str(e)}", "ERROR")
        raise HTTPException(status_code=500, detail="Failed to retrieve intake history")