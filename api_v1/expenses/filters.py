from fastapi import Depends, HTTPException, Query
from datetime import datetime, timedelta
from typing import Optional

class ExpenseFilter:
    def __init__(
        self,
        period: Optional[str] = Query(default=None, enum=["week", "month", "3months", "custom"]),
        start_date: Optional[datetime] = Query(default=None),
        end_date: Optional[datetime] = Query(default=None)
    ):
        now = datetime.utcnow()

        if period == "week":
            self.start_date = now - timedelta(days=7)
            self.end_date = now
        elif period == "month":
            self.start_date = now - timedelta(days=30)
            self.end_date = now
        elif period == "3months":
            self.start_date = now - timedelta(days=90)
            self.end_date = now
        elif period == "custom":
            if not (start_date and end_date):
                raise HTTPException(status_code=400, detail="Custom period requires both start_date and end_date")
            self.start_date = start_date
            self.end_date = end_date
        else:
            self.start_date = None
            self.end_date = None
