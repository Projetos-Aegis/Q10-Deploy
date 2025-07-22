from flask import Flask, jsonify, request
import psycopg2

app = Flask(__name__)

DB_CONFIG = {
    "host": "aws-0-us-east-1.pooler.supabase.com",
    "port": 5432,
    "database": "postgres",
    "user": "postgres.zbovdvkexpyprgiibszm",
    "password": "7H?9@63VWjkp*wh"
}

def get_kpi_data(time_range):
    if time_range == "1 hour":
        interval = "1 hour"
    elif time_range == "24 hour":
        interval = "24 hour"
    elif time_range == "7 day":
        interval = "7 day"
    else:
        interval = "1 hour"

    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    query = f"""
        SELECT duracao_contato, tempo_entre_respostas, tempo_primeira_resposta,
               nota_satisfacao, tipo_fila, atendente
        FROM kpis_atendimento
        WHERE data_contato >= NOW() - INTERVAL '{interval}'
    """
    cur.execute(query)
    rows = cur.fetchall()
    conn.close()

    raw_data = []
    for row in rows:
        raw_data.append({
            "duracao_contato": row[0] or 0,
            "tempo_entre_respostas": row[1] or 0,
            "tempo_primeira_resposta": row[2] or 0,
            "nota_satisfacao": row[3],
            "tipo_fila": row[4] or "",
            "atendente": row[5] or ""
        })
    return raw_data

@app.route('/api/kpis')
def kpis():
    time_range = request.args.get('timeRange', '1 hour')
    raw_data = get_kpi_data(time_range)
    if not raw_data:
        return jsonify({
            "tma": 0, "tme": 0, "firstResponse": 0, "lastResponse": 0,
            "queueWait": 0, "inactivity": 0, "abandonment": 0, "csat": 0,
            "responseRate": 0, "topQueues": [],
            "agentStatus": {"available": 0, "paused": 0, "busy": 0},
            "queuesWithMostAgents": [], "queuesWithMostEntries": [],
            "queuesWithHighestTMA": [], "queuesWithHighestTME": []
        })

    tma = round(sum(d['duracao_contato'] for d in raw_data) / len(raw_data))
    tme = round(sum(d['tempo_entre_respostas'] for d in raw_data) / len(raw_data))
    first_response = round(sum(d['tempo_primeira_resposta'] for d in raw_data) / len(raw_data))
    total_ratings = len([d for d in raw_data if d.get('nota_satisfacao')])
    positive_ratings = len([d for d in raw_data if d.get('nota_satisfacao', 0) >= 4])
    csat = round((positive_ratings / total_ratings) * 100) if total_ratings > 0 else 0

    from collections import Counter
    queue_counts = Counter(d['tipo_fila'] for d in raw_data)
    top_queues = [{"name": k, "calls": v} for k, v in queue_counts.most_common(3)]

    agent_status = {d['atendente']: True for d in raw_data if d.get('atendente')}
    agent_count = len(agent_status)

    result = {
        "tma": tma,
        "tme": tme,
        "firstResponse": first_response,
        "lastResponse": tme,
        "queueWait": tme,
        "inactivity": 0,
        "abandonment": 0,
        "csat": csat,
        "responseRate": 100,
        "topQueues": top_queues,
        "agentStatus": {
            "available": agent_count,
            "paused": 0,
            "busy": 0
        },
        "queuesWithMostAgents": [{"name": q["name"], "agents": q["calls"] // 3} for q in top_queues],
        "queuesWithMostEntries": top_queues,
        "queuesWithHighestTMA": [{"name": q["name"], "tma": tma} for q in top_queues],
        "queuesWithHighestTME": [{"name": q["name"], "tme": tme} for q in top_queues]
    }
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)