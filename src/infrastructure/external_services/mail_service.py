"""
メール送信サービス
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Optional
from app.config import settings


class MailService:
    """メール送信サービス"""
    
    def __init__(self):
        self.smtp_server = settings.MAIL_SERVER
        self.smtp_port = settings.MAIL_PORT
        self.username = settings.MAIL_USERNAME
        self.password = settings.MAIL_PASSWORD
    
    def send_email(
        self, 
        to_addresses: List[str], 
        subject: str, 
        body: str, 
        from_address: Optional[str] = None
    ) -> bool:
        """メールを送信する"""
        if not self.smtp_server or not self.username or not self.password:
            print("メール設定が不完全です。メール送信をスキップします。")
            return False
        
        try:
            # メールメッセージを作成
            msg = MIMEMultipart()
            msg['From'] = from_address or self.username
            msg['To'] = ', '.join(to_addresses)
            msg['Subject'] = subject
            
            # 本文を追加
            msg.attach(MIMEText(body, 'plain', 'utf-8'))
            
            # SMTPサーバーに接続してメールを送信
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.username, self.password)
                server.send_message(msg)
            
            print(f"メール送信成功: {subject} -> {to_addresses}")
            return True
            
        except Exception as e:
            print(f"メール送信エラー: {e}")
            return False
    
    def send_welcome_email(self, user_email: str, user_name: str) -> bool:
        """ウェルカムメールを送信する"""
        subject = "アカウント登録完了のお知らせ"
        body = f"""
{user_name} 様

アカウントの登録が完了いたしました。
ご利用いただき、ありがとうございます。

今後ともよろしくお願いいたします。
        """.strip()
        
        return self.send_email([user_email], subject, body)
    
    def send_password_reset_email(self, user_email: str, reset_token: str) -> bool:
        """パスワードリセットメールを送信する"""
        subject = "パスワードリセットのお知らせ"
        body = f"""
パスワードリセットのリクエストを受け付けました。

以下のリンクからパスワードをリセットしてください：
https://example.com/reset-password?token={reset_token}

このリンクの有効期限は24時間です。

もしこのリクエストを送信していない場合は、このメールを無視してください。
        """.strip()
        
        return self.send_email([user_email], subject, body)
