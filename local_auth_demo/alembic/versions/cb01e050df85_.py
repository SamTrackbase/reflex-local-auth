"""empty message

Revision ID: cb01e050df85
Revises: 05267fabef38
Create Date: 2024-04-10 13:12:57.109831

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel

# revision identifiers, used by Alembic.
revision: str = 'cb01e050df85'
down_revision: Union[str, None] = '05267fabef38'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('localauthsession',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('session_id', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('expiration', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_localauthsession_session_id'), 'localauthsession', ['session_id'], unique=True)
    op.create_index(op.f('ix_localauthsession_user_id'), 'localauthsession', ['user_id'], unique=False)
    op.create_table('localuser',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('password_hash', sa.LargeBinary(), nullable=False),
    sa.Column('enabled', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_localuser_username'), 'localuser', ['username'], unique=True)
    op.execute("INSERT INTO localuser SELECT * FROM user;")
    op.execute("INSERT INTO localauthsession SELECT * FROM authsession;")
    op.drop_index('ix_authsession_session_id', table_name='authsession')
    op.drop_index('ix_authsession_user_id', table_name='authsession')
    op.drop_table('authsession')
    naming_convention = {
        "fk":
        "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    }
    with op.batch_alter_table('userinfo', naming_convention=naming_convention) as batch_op:
        batch_op.drop_constraint('fk_userinfo_user_id_user', type_='foreignkey')
        batch_op.create_foreign_key('fk_userinfo_user_id_localuser', 'localuser', ['user_id'], ['id'])
    op.drop_index('ix_user_username', table_name='user')
    op.drop_table('user')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('username', sa.VARCHAR(), nullable=False),
    sa.Column('password_hash', sa.BLOB(), nullable=False),
    sa.Column('enabled', sa.BOOLEAN(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_user_username', 'user', ['username'], unique=1)
    op.create_table('authsession',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('user_id', sa.INTEGER(), nullable=False),
    sa.Column('session_id', sa.VARCHAR(), nullable=False),
    sa.Column('expiration', sa.DATETIME(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_authsession_user_id', 'authsession', ['user_id'], unique=False)
    op.create_index('ix_authsession_session_id', 'authsession', ['session_id'], unique=1)
    op.execute("INSERT INTO user SELECT * FROM localuser;")
    op.execute("INSERT INTO authsession SELECT * FROM localauthsession;")
    naming_convention = {
        "fk":
        "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    }
    with op.batch_alter_table('userinfo', naming_convention=naming_convention) as batch_op:
        batch_op.drop_constraint('fk_userinfo_user_id_localuser', type_='foreignkey')
        batch_op.create_foreign_key('fk_userinfo_user_id_user', 'localuser', ['user_id'], ['id'])
    op.drop_index(op.f('ix_localuser_username'), table_name='localuser')
    op.drop_table('localuser')
    op.drop_index(op.f('ix_localauthsession_user_id'), table_name='localauthsession')
    op.drop_index(op.f('ix_localauthsession_session_id'), table_name='localauthsession')
    op.drop_table('localauthsession')
    # ### end Alembic commands ###