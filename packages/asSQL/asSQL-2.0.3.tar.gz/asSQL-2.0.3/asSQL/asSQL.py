import sqlite3, json, re
def jsonify(data):
    
    json_string = data
    return json_string

class Client:
    def __init__(self,username):
        self.username = username
        
        
        
    def __getitem__(self, key):
        return TableAPI(self.username, key)
        
        
class TableAPI:
    def __init__(self,username,table_name):
        self.username = username
        self.table_name = table_name
        
        
    def create_table(self):
        try:
            connection = sqlite3.connect('database.db', check_same_thread=False)
            c = connection.cursor()
            c.execute(f"SELECT count(name) FROM sqlite_master WHERE type='table' AND name LIKE '{self.username}_%'")
            count = c.fetchone()[0]
            if count < 5:
                c.execute(f"CREATE TABLE IF NOT EXISTS {self.username}_{self.table_name} (key TEXT PRIMARY KEY, value TEXT)")
                
                connection.commit()
                connection.close()
                return jsonify(True)
            else:
                return jsonify("You have reached the maximum number of allowed tables (5)")
        except Exception as e:
            return jsonify(False)
  
            
    def set(self, key, value):
        connection = sqlite3.connect('database.db', check_same_thread=False)
        c = connection.cursor()
        c.execute(f"INSERT OR REPLACE INTO {self.username}_{self.table_name} (key, value) VALUES (?, ?)", (key, json.dumps(value)))
        connection.commit()
        connection.close()
        return jsonify(True)

    def get(self,key):
        try:
            connection = sqlite3.connect('database.db', check_same_thread=False)
            c = connection.cursor()
            c.execute(f"SELECT value FROM {self.username}_{self.table_name} WHERE key=?", (key,))
            result = c.fetchone()
            connection.close()
            if result:
                
                return jsonify(json.loads(result[0]))
                
            else:
                
                return jsonify(None)
        except sqlite3.OperationalError:
            connection.close()
            return jsonify(None)

    def delete(self, key):
        try:
            connection = sqlite3.connect('database.db', check_same_thread=False)
            c = connection.cursor()
            c.execute(f"DELETE FROM {self.username}_{self.table_name} WHERE key = ?", (key,))
            connection.commit()
            connection.close()
            return jsonify(True)
        except sqlite3.OperationalError:
            connection.close()
            return jsonify(False)
            
    def get_all(self):
        try:
            connection = sqlite3.connect('database.db', check_same_thread=False)
            c = connection.cursor()
            c.execute(f"SELECT * FROM {self.username}_{self.table_name}")
            data = c.fetchall()
            connection.close()
            if data:
                result = []
                for item in data:
                    key = item[0]
                    value = json.loads(item[1])
                    if type(value) is dict:
                        result.append(f"- {key}\n ├ {value}\n └ Dict.\n")
                    elif type(value) is str:
                        result.append(f"- {key}\n ├ {value}\n └ Str.\n")
                    elif type(value) is bool:
                        result.append(f"- {key}\n ├ {value}\n └ Bool.\n")
                    else:
                        result.append(f"- {key}\n ├ {value}\n └ {type(value)}.\n")
                    
                return jsonify("".join(result))
                
            else:
                
                return jsonify(None)
        except Exception as e:
            connection.close()
            return jsonify(str(e))
    def tables(self):
        try:
            connection = sqlite3.connect('database.db', check_same_thread=False)
            c = connection.cursor()
            c.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name LIKE '{self.username}_%'")
            tables = c.fetchall()
            
            prefix = len(f"{self.username}_")
            user_tables = [table[0][prefix:] for table in tables]
            connection.close()
            return user_tables
        except sqlite3.OperationalError:
            connection.close()
            return None    
    

    def keys(self,pattern=None,list=None):
        try:
            connection = sqlite3.connect('database.db', check_same_thread=False)
            c = connection.cursor()
            c.execute(f"SELECT key FROM {self.username}_{self.table_name}")
            data = c.fetchall()
            
            if data:
                keys = []
                for item in data:
                    if pattern:
                        pattern = pattern.replace("*", ".*")
                        if re.match(pattern, item[0]):
                            keys.append(item[0])
                    else:
                        keys.append(item[0])
                if list:
                    connection.close()
                    return keys
                else:
                    connection.close()
                    return jsonify("\n".join(keys))
                
            else:
                connection.close()
                return jsonify(None)
        except Exception as e:
            connection.close()
            return jsonify(str(e))
    
    def key_exists(self, key):
            connection = sqlite3.connect('database.db', check_same_thread=False)
            c = connection.cursor()
            c.execute(f"SELECT 1 FROM {self.username}_{self.table_name} WHERE key=?", (key,))
            result = c.fetchone()
        
            connection.close()
            
            if result:
                return 1
            else:
                return 0
    
    def push(self, key, value):
        try:
            connection = sqlite3.connect('database.db', check_same_thread=False)
            c = connection.cursor()
            c.execute(f"SELECT value FROM {self.username}_{self.table_name} WHERE key=?", (key,))
            data = c.fetchone()
            
            if data:
                json_data = json.loads(data[0])
                if isinstance(json_data, list):
                    json_data.append(value)
                    c.execute(f"UPDATE {self.username}_{self.table_name} SET value = ? WHERE key = ?", (json.dumps(json_data), key))
                    connection.commit()
                    connection.close()
                    return True
                else:
                    return "The value stored at this key is not a list"
            else:
                return "Key does not exist"
        except Exception as e:
            connection.close()
            return str(e)
    
    def unpush(self, key, value):
        try:
            connection = sqlite3.connect('database.db', check_same_thread=False)
            c = connection.cursor()
            c.execute(f"SELECT value FROM {self.username}_{self.table_name} WHERE key=?", (key,))
            data = c.fetchone()
           
            if data:
                json_data = json.loads(data[0])
                if isinstance(json_data, list):
                    json_data.remove(value)
                    c.execute(f"UPDATE {self.username}_{self.table_name} SET value = ? WHERE key = ?", (json.dumps(json_data), key))
                    connection.commit()
                    connection.close()
                    return True
                else:
                    return "The value stored at this key is not a list"
            else:
                return "Key does not exist"
        except ValueError:
            return "Value is not in list"
    
