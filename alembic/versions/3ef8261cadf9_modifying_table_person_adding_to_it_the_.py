"""modifying table person, adding to it the user and password columns

Revision ID: 3ef8261cadf9
Revises: 7fd94f41ee94
Create Date: 2024-08-27 20:09:51.647238

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3ef8261cadf9'
down_revision: Union[str, None] = '7fd94f41ee94'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('administrador_usuario_key', 'administrador', type_='unique')
    op.drop_column('administrador', 'password')
    op.drop_column('administrador', 'usuario')
    op.add_column('candidato', sa.Column('nombres', sa.String(), nullable=False))
    op.add_column('candidato', sa.Column('apellido_paterno', sa.String(), nullable=False))
    op.add_column('candidato', sa.Column('apellido_materno', sa.String(), nullable=False))
    op.drop_constraint('candidato_id_persona_fkey', 'candidato', type_='foreignkey')
    op.drop_column('candidato', 'id_persona')
    op.drop_constraint('elector_usuario_key', 'elector', type_='unique')
    op.drop_column('elector', 'password')
    op.drop_column('elector', 'usuario')
    op.add_column('persona', sa.Column('usuario', sa.String(), nullable=True))
    op.add_column('persona', sa.Column('password', sa.String(), nullable=False))
    op.create_unique_constraint(None, 'persona', ['usuario'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'persona', type_='unique')
    op.drop_column('persona', 'password')
    op.drop_column('persona', 'usuario')
    op.add_column('elector', sa.Column('usuario', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.add_column('elector', sa.Column('password', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.create_unique_constraint('elector_usuario_key', 'elector', ['usuario'])
    op.add_column('candidato', sa.Column('id_persona', sa.INTEGER(), autoincrement=False, nullable=False))
    op.create_foreign_key('candidato_id_persona_fkey', 'candidato', 'persona', ['id_persona'], ['id'], ondelete='CASCADE')
    op.drop_column('candidato', 'apellido_materno')
    op.drop_column('candidato', 'apellido_paterno')
    op.drop_column('candidato', 'nombres')
    op.add_column('administrador', sa.Column('usuario', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.add_column('administrador', sa.Column('password', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.create_unique_constraint('administrador_usuario_key', 'administrador', ['usuario'])
    # ### end Alembic commands ###