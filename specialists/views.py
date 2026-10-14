from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from db.database import get_connection


def specialists(request: HttpRequest) -> HttpResponse:
    conn = get_connection()
    rows = conn.execute(
        """
        SELECT id, first_name, last_name, speciality, experience_years
        FROM specialists
        ORDER BY last_name
        """
    ).fetchall()
    conn.close()

    return render(
        request,
        'specialists/specialist_list.html',
        {'specialists': [dict(row) for row in rows]},
    )


def specialist_detail(
    request: HttpRequest, specialist_id: int,
) -> HttpResponse:
    conn = get_connection()
    row = conn.execute(
        """
        SELECT id, first_name, last_name, speciality,
               phone, email, experience_years
        FROM specialists
        WHERE id = ?
        """,
        [specialist_id],
    ).fetchone()
    conn.close()

    if row is None:
        return render(
            request,
            'specialists/specialist_not_found.html',
            status=404,
        )

    return render(
        request,
        'specialists/specialist_detail.html',
        {'specialist': dict(row)},
    )