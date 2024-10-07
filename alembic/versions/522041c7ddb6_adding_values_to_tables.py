"""adding values to tables

Revision ID: 522041c7ddb6
Revises: 8bc15a196b47
Create Date: 2024-10-07 17:31:39.340902

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '522041c7ddb6'
down_revision: Union[str, None] = '8bc15a196b47'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
       INSERT INTO eleccion (id, fecha, hora_inicio, hora_fin, descripcion) VALUES
       (1, '2024-12-01 00:00:00+00', '08:00:00', '18:00:00', 'Eleccion Presidencial'),
       (2, '2024-12-15 00:00:00+00', '08:00:00', '18:00:00', 'Eleccion Regional');
       """)

    # Insert 3 lists for each election (total of 6 lists)
    op.execute("""
       INSERT INTO lista (id, nombre, id_eleccion, propuesta) VALUES
       (1, 'Lista 1 Eleccion 1', 1, 'Propuesta A de Lista 1 Eleccion 1'),
       (2, 'Lista 2 Eleccion 1', 1, 'Propuesta B de Lista 2 Eleccion 1'),
       (3, 'Lista 3 Eleccion 1', 1, 'Propuesta C de Lista 3 Eleccion 1'),
       (4, 'Lista 1 Eleccion 2', 2, 'Propuesta A de Lista 1 Eleccion 2'),
       (5, 'Lista 2 Eleccion 2', 2, 'Propuesta B de Lista 2 Eleccion 2'),
       (6, 'Lista 3 Eleccion 2', 2, 'Propuesta C de Lista 3 Eleccion 2');
       """)

    # Insert 4 candidates for each list (total of 24 candidates)
    op.execute("""
       INSERT INTO candidato (id, nombres, apellido_paterno, apellido_materno, id_lista) VALUES
       (1, 'Candidato 1', 'ApellidoP1', 'ApellidoM1', 1),
       (2, 'Candidato 2', 'ApellidoP2', 'ApellidoM2', 1),
       (3, 'Candidato 3', 'ApellidoP3', 'ApellidoM3', 1),
       (4, 'Candidato 4', 'ApellidoP4', 'ApellidoM4', 1),

       (5, 'Candidato 1', 'ApellidoP1', 'ApellidoM1', 2),
       (6, 'Candidato 2', 'ApellidoP2', 'ApellidoM2', 2),
       (7, 'Candidato 3', 'ApellidoP3', 'ApellidoM3', 2),
       (8, 'Candidato 4', 'ApellidoP4', 'ApellidoM4', 2),

       (9, 'Candidato 1', 'ApellidoP1', 'ApellidoM1', 3),
       (10, 'Candidato 2', 'ApellidoP2', 'ApellidoM2', 3),
       (11, 'Candidato 3', 'ApellidoP3', 'ApellidoM3', 3),
       (12, 'Candidato 4', 'ApellidoP4', 'ApellidoM4', 3),

       (13, 'Candidato 1', 'ApellidoP1', 'ApellidoM1', 4),
       (14, 'Candidato 2', 'ApellidoP2', 'ApellidoM2', 4),
       (15, 'Candidato 3', 'ApellidoP3', 'ApellidoM3', 4),
       (16, 'Candidato 4', 'ApellidoP4', 'ApellidoM4', 4),

       (17, 'Candidato 1', 'ApellidoP1', 'ApellidoM1', 5),
       (18, 'Candidato 2', 'ApellidoP2', 'ApellidoM2', 5),
       (19, 'Candidato 3', 'ApellidoP3', 'ApellidoM3', 5),
       (20, 'Candidato 4', 'ApellidoP4', 'ApellidoM4', 5),

       (21, 'Candidato 1', 'ApellidoP1', 'ApellidoM1', 6),
       (22, 'Candidato 2', 'ApellidoP2', 'ApellidoM2', 6),
       (23, 'Candidato 3', 'ApellidoP3', 'ApellidoM3', 6),
       (24, 'Candidato 4', 'ApellidoP4', 'ApellidoM4', 6);
       """)

def downgrade() -> None:
    # Delete candidates (total of 24 candidates)
    op.execute("""
    DELETE FROM candidato WHERE id IN (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12,
                                       13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24);
    """)

    # Delete lists (total of 6 lists)
    op.execute("""
    DELETE FROM lista WHERE id IN (1, 2, 3, 4, 5, 6);
    """)

    # Delete elections (total of 2 elections)
    op.execute("""
    DELETE FROM eleccion WHERE id IN (1, 2);
    """)

