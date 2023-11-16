
@app.route('/')
    def dashboard():
        mydb = db.get_db()
        rows = mydb.execute(
            "SELECT * FROM ITEMS"
        ).fetchall()

        current_items = [FridgeItem(r["name"],
                                    r["expiry_time"],
                                    db_convert_isodate(r["date_added"]),
                                    db_convert_isodate(r["expiry_date"]))
                         for r in rows]
        #breakpoint()
        return render_template("dashboard.html", current_items=current_items)
