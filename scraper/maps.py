def map_team_jumps(row):
    return (
        {
            "distance": float(row[-5]),
            "total_points": row[-4]
        },
        {
            "distance": float(row[-3]),
            "total_points": float(row[-2])
        } if row[-3] else None
    )


def map_detailed_jump(row):
    return {
        "distance": float(row[3]),
        "distance_points": float(row[4]),
        "speed": float(row[1]),
        "judge_a": float(row[6]),
        "judge_b": float(row[7]),
        "judge_c": float(row[8]),
        "judge_d": float(row[9]),
        "judge_e": float(row[10]),
        "judge_points": float(row[11]),
        "gate": int(row[13]),
        "gate_points": float(row[14]),
        "wind": float(row[15]),
        "wind_points": float(row[16]),
        "total_points": float(row[18]),
        "rank": int(row[19]),
    }


def map_simple_jump(row):
    if len(row) > 9:
        return (
            {
                "distance": float(row[-10]),
                "total_points": float(row[-8])
            } if row[-10] else None,
            {
                "distance": float(row[-5]),
                "total_points": float(row[-3])
            } if row[-5] else None,
        )
    return None, None


def map_simple_jumper(row):
    if len(row) > 9:
        return {
            "fis_code": int(row[2]),
            "name": row[3],
            "born": int(row[4]),
        }
    return {
        "fis_code": int(row[1]),
        "name": row[2],
        "born": int(row[3]) if row[3] else 0,
    }


def map_details_jumper(row):
    return {
        "name": row[2],
    }


def map_team_jumper(row):
    return {
        "fis_code": int(row[1]),
        "name": row[2],
        "born": int(row[3]),
    }


def map_team_country(row):
    return {
        "fis_code": int(row[1]),
        "name": row[4],
    }


def map_jumper_country_detail(row):
    return {
        "name": row[4]
    }


def map_jumper_country_simple(row):
    return {
        "name": row[5]
    }


def map_other_params_detail(row):
    return {
        "rank": int(row[0]) if row[0] else "",
        "bib": int(row[1]),
        "total_points": float(row[-1])
    }


def map_diff_detail(row):
    try:
        return {"diff": float(row[-1])}
    except ValueError:
        return {"diff": None}


def map_other_params_simple(row):
    if len(row) > 9:
        return {
            "rank": int(row[0]),
            "bib": int(row[1]),
            "total_points": float(row[-2]),
            "diff": float(row[-1]) if row[-1] else None
        }
    return {
        "rank": int(row[0]),
        "total_points": float(row[-2]),
        "diff": float(row[-1]) if row[-1] else None
    }


def map_country_as_participant(row):
    return {
        "rank": int(row[0]),
        "total_points": float(row[-1])
    }
