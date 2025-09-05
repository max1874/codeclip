import sqlite3
import re
import time
from pathlib import Path
import pyperclip
from typing import Optional

class Message:
    def __init__(self, message_date: int, text: str):
        self.message_date = message_date
        self.text = text

class SMSCodeExtractor:
    def __init__(self):
        self.db_path = str(Path.home() / "Library/Messages/chat.db")
        self.db = None
        self.update_time = 0
        # 默认的验证码匹配模式：4, 5, 6位数字
        self.code_pattern = r'(?<!\d)(\d{4}|\d{5}|\d{6})(?!\d)'
    
    def open_database(self) -> bool:
        try:
            self.db = sqlite3.connect(self.db_path)
            return True
        except sqlite3.Error as e:
            print(f"Error accessing Messages database: {e}")
            print("Please grant Full Disk Access permission in System Preferences > Security & Privacy")
            return False
    
    def get_latest_message(self) -> Optional[Message]:
        if not self.db:
            return None
            
        sql = """
        SELECT
            (message.date / 1000000000 + 978307200) AS message_date,
            message.text
        FROM
            message
                LEFT JOIN chat_message_join
                        ON chat_message_join.message_id = message.ROWID
                LEFT JOIN chat
                        ON chat.ROWID = chat_message_join.chat_id
                LEFT JOIN handle
                        ON message.handle_id = handle.ROWID
        WHERE
            is_from_me = 0
            AND text IS NOT NULL
            AND length(text) > 0
            AND (
                text GLOB '*[0-9][0-9][0-9][0-9]*'
                OR text GLOB '*[0-9][0-9][0-9][0-9][0-9]*'
                OR text GLOB '*[0-9][0-9][0-9][0-9][0-9][0-9]*'
                OR text GLOB '*[0-9][0-9][0-9][0-9][0-9][0-9][0-9]*'
                OR text GLOB '*[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]*'
            )
        ORDER BY
            message.date DESC
        LIMIT 1
        """
        
        try:
            cursor = self.db.cursor()
            cursor.execute(sql)
            row = cursor.fetchone()
            if row:
                return Message(int(row[0]), row[1])
        except sqlite3.Error as e:
            print(f"Database error: {e}")
        return None
    
    def extract_code(self, message: Message) -> Optional[str]:
        if not message:
            return None
        
        try:
            match = re.search(self.code_pattern, message.text)
            if match:
                return match.group(1)
        except re.error:
            print("Invalid regex pattern")
        
        return None
    
    def run(self):
        if not self.open_database():
            return
        
        print("SMS Code Extractor is running...")
        print("Monitoring for new messages...")
        
        try:
            while True:
                message = self.get_latest_message()
                # print(message.text)
                if message and message.message_date != self.update_time:
                    self.update_time = message.message_date
                    code = self.extract_code(message)
                    if code:
                        pyperclip.copy(code)
                        print(f"Found new code: {code} (copied to clipboard)")
                time.sleep(5)  # 检查间隔2秒
                
        except KeyboardInterrupt:
            print("\nStopping SMS Code Extractor...")
        finally:
            if self.db:
                self.db.close()

if __name__ == "__main__":
    extractor = SMSCodeExtractor()
    extractor.run()