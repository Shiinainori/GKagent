#!/usr/bin/env python3
"""浙江省普通类高考志愿数据库查询脚本"""

import argparse
import json
import sqlite3
import sys
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "assets" / "gk_data.db"


def get_connection():
    if not DB_PATH.exists():
        print(json.dumps({"error": f"数据库文件不存在: {DB_PATH}，请先导入录取数据"}, ensure_ascii=False))
        sys.exit(1)
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn


def rank_lookup(score: int):
    """根据分数查浙江省全省位次"""
    conn = get_connection()
    cur = conn.execute(
        "SELECT rank, count FROM rank_table "
        "WHERE province='浙江' AND score=? "
        "ORDER BY year DESC LIMIT 1",
        (score,),
    )
    row = cur.fetchone()
    conn.close()

    if row is None:
        return {"error": f"未找到浙江分数 {score} 的位次数据"}
    return {"score": score, "rank": row["rank"], "count": row["count"]}


def check_subject_match(subject_requirement: str, student_subjects: str) -> bool:
    """检查考生选考科目是否满足专业要求"""
    if not subject_requirement or subject_requirement == "不限":
        return True

    required = [s.strip() for s in subject_requirement.replace("必选", "").split("+")]
    student_list = [s.strip() for s in student_subjects.split("+")]

    for req in required:
        if req and req not in student_list:
            return False
    return True


def query_volunteers(subjects: str, rank_min: int, rank_max: int, label: str):
    """按位次范围查询志愿，并过滤选考科目"""
    conn = get_connection()
    cur = conn.execute(
        """
        SELECT province, school_code, school_name, major_code, major_name,
               subject_requirement, plan_count, score, rank
        FROM admission_data
        WHERE province = '浙江'
          AND rank BETWEEN ? AND ?
        ORDER BY rank ASC
        LIMIT 80
        """,
        (rank_min, rank_max),
    )
    rows = [dict(r) for r in cur.fetchall()]
    conn.close()

    matched = []
    unmatched = []
    for r in rows:
        r["label"] = label
        if check_subject_match(r.get("subject_requirement", ""), subjects):
            r["subject_match"] = True
            matched.append(r)
        else:
            r["subject_match"] = False
            unmatched.append(r)

    return {"matched": matched, "unmatched": unmatched}


def main():
    parser = argparse.ArgumentParser(description="浙江省普通类高考志愿数据库查询")
    parser.add_argument("--action", required=True, choices=["rank_lookup", "query"])
    parser.add_argument("--province", default="浙江")
    parser.add_argument("--score", type=int, default=0)
    parser.add_argument("--subjects", default="", help="考生选考科目，如 物理+化学+生物")
    parser.add_argument("--rank-min", type=int, default=0)
    parser.add_argument("--rank-max", type=int, default=0)
    parser.add_argument("--label", default="", help="冲稳保标签: rush/stable/safe")
    args = parser.parse_args()

    if args.action == "rank_lookup":
        result = rank_lookup(args.score)
    elif args.action == "query":
        result = query_volunteers(args.subjects, args.rank_min, args.rank_max, args.label)
    else:
        result = {"error": f"未知 action: {args.action}"}

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
