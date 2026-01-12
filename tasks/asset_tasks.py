from datetime import datetime, timedelta
from datetime import datetime, timedelta
from extensions import scheduler
from models.assignment import AssetAssignment

def asset_return_reminder(app):
    with app.app_context(): 
        overdue_assets = AssetAssignment.query.filter(
            AssetAssignment.released_at == None,
            AssetAssignment.assigned_at < datetime.utcnow() - timedelta(days=1)
        ).all()

        if overdue_assets:
            print("Overdue assets:")
            for a in overdue_assets:
                print(f"Asset ID {a.asset_id} assigned to Employee {a.employee_id}")
        else:
            print("No overdue assets")
