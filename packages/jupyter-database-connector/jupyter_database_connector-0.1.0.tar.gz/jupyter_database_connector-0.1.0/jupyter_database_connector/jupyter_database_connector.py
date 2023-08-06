from jupyter_server.base.handlers import BaseHandler
import sqlalchemy as db

class DatabaseHandler(BaseHandler):
    async def get(self):
        # Connect to the database
        engine = db.create_engine('sqlite:///example.db')
        connection = engine.connect()

        # Execute a SELECT statement
        query = db.select([db.text("* from example_table")])
        result = connection.execute(query)

        # Convert the result to a JSON-serializable format
        response = [dict(row) for row in result]

        # Return the result to the client
        self.write(response)

    async def post(self):
        # Connect to the database
        engine = db.create_engine('sqlite:///example.db')
        connection = engine.connect()

        # Extract the data from the request body
        data = self.get_json()

        # Execute an INSERT statement
        query = db.insert(db.text("example_table")).values(**data)
        result = connection.execute(query)

        # Return the result to the client
        self.write({'status': 'success'})