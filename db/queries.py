class Queries:
    CREATE_SURVEY_TABLE = """
     CREATE TABLE IF NOT EXISTS results_oprosa(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    age INTEGER,
    occupation TEXT,
    salary_or_grade TEXT
    )
    """
