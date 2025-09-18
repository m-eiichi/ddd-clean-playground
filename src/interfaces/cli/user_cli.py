"""
ユーザーCLI
"""
import click
from sqlalchemy.orm import Session
from application.dtos.user_dto import UserCreateDTO
from application.services.user_app_service import UserAppService
from infrastructure.repositories.user_repository_impl import UserRepositoryImpl
from infrastructure.db.session import db_session


def get_user_service() -> UserAppService:
    """ユーザーアプリケーションサービスを取得"""
    db = db_session.get_session()
    try:
        user_repository = UserRepositoryImpl(db)
        return UserAppService(user_repository)
    finally:
        db.close()


@click.group()
def user_cli():
    """ユーザー管理CLI"""
    pass


@user_cli.command()
@click.option('--email', required=True, help='メールアドレス')
@click.option('--name', required=True, help='ユーザー名')
def create(email: str, name: str):
    """ユーザーを作成する"""
    try:
        user_service = get_user_service()
        dto = UserCreateDTO(email=email, name=name)
        user = user_service.create_user(dto)
        
        click.echo(f"ユーザーを作成しました:")
        click.echo(f"  ID: {user.id}")
        click.echo(f"  メールアドレス: {user.email}")
        click.echo(f"  名前: {user.name}")
        click.echo(f"  作成日時: {user.created_at}")
        
    except ValueError as e:
        click.echo(f"エラー: {e}", err=True)
    except Exception as e:
        click.echo(f"予期しないエラー: {e}", err=True)


@user_cli.command()
@click.option('--user-id', type=int, help='ユーザーID')
@click.option('--email', help='メールアドレス')
def get(user_id: int = None, email: str = None):
    """ユーザーを取得する"""
    if not user_id and not email:
        click.echo("ユーザーIDまたはメールアドレスを指定してください", err=True)
        return
    
    try:
        user_service = get_user_service()
        
        if user_id:
            user = user_service.get_user_by_id(user_id)
        else:
            user = user_service.get_user_by_email(email)
        
        if user is None:
            click.echo("ユーザーが見つかりません", err=True)
            return
        
        click.echo(f"ユーザー情報:")
        click.echo(f"  ID: {user.id}")
        click.echo(f"  メールアドレス: {user.email}")
        click.echo(f"  名前: {user.name}")
        click.echo(f"  作成日時: {user.created_at}")
        click.echo(f"  更新日時: {user.updated_at}")
        
    except Exception as e:
        click.echo(f"エラー: {e}", err=True)


@user_cli.command()
@click.option('--page', type=int, default=1, help='ページ番号')
@click.option('--per-page', type=int, default=10, help='1ページあたりの件数')
def list_users(page: int, per_page: int):
    """ユーザー一覧を表示する"""
    try:
        user_service = get_user_service()
        result = user_service.get_users(page, per_page)
        
        click.echo(f"ユーザー一覧 (全{result.total_count}件, ページ{result.page}/{result.total_count // result.per_page + 1}):")
        click.echo("-" * 80)
        
        for user in result.users:
            click.echo(f"ID: {user.id:3d} | {user.email:30s} | {user.name:20s} | {user.created_at.strftime('%Y-%m-%d %H:%M')}")
        
    except Exception as e:
        click.echo(f"エラー: {e}", err=True)


@user_cli.command()
@click.option('--user-id', type=int, required=True, help='ユーザーID')
@click.option('--name', help='新しいユーザー名')
@click.option('--email', help='新しいメールアドレス')
def update(user_id: int, name: str = None, email: str = None):
    """ユーザーを更新する"""
    if not name and not email:
        click.echo("更新する項目（名前またはメールアドレス）を指定してください", err=True)
        return
    
    try:
        from application.dtos.user_dto import UserUpdateDTO
        
        user_service = get_user_service()
        dto = UserUpdateDTO(name=name, email=email)
        user = user_service.update_user(user_id, dto)
        
        if user is None:
            click.echo("ユーザーが見つかりません", err=True)
            return
        
        click.echo(f"ユーザーを更新しました:")
        click.echo(f"  ID: {user.id}")
        click.echo(f"  メールアドレス: {user.email}")
        click.echo(f"  名前: {user.name}")
        click.echo(f"  更新日時: {user.updated_at}")
        
    except ValueError as e:
        click.echo(f"エラー: {e}", err=True)
    except Exception as e:
        click.echo(f"予期しないエラー: {e}", err=True)


@user_cli.command()
@click.option('--user-id', type=int, required=True, help='ユーザーID')
@click.confirmation_option(prompt='本当に削除しますか？')
def delete(user_id: int):
    """ユーザーを削除する"""
    try:
        user_service = get_user_service()
        success = user_service.delete_user(user_id)
        
        if success:
            click.echo(f"ユーザーID {user_id} を削除しました")
        else:
            click.echo("ユーザーが見つかりません", err=True)
        
    except Exception as e:
        click.echo(f"エラー: {e}", err=True)


@user_cli.command()
def stats():
    """統計情報を表示する"""
    try:
        user_service = get_user_service()
        count = user_service.get_active_users_count()
        
        click.echo(f"アクティブユーザー数: {count}")
        
    except Exception as e:
        click.echo(f"エラー: {e}", err=True)


if __name__ == '__main__':
    user_cli()
