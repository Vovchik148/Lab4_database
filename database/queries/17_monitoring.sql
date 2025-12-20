CREATE EXTENSION IF NOT EXISTS pg_stat_statements;

SELECT 
    'Cache Hit Ratio' as metric,
    round(sum(blks_hit) * 100.0 / sum(blks_hit + blks_read), 2) || '%' as ratio
FROM pg_stat_database;

SELECT 
    round(mean_exec_time::numeric, 2) as avg_time_ms,
    calls as execution_count,
    rows as rows_per_call,
    round(total_exec_time::numeric, 2) as total_time_ms,
    substring(query, 1, 150) as query_preview
FROM pg_stat_statements
ORDER BY mean_exec_time DESC
LIMIT 10;

SELECT 
    schemaname,
    relname as "table",
    indexrelname as "index",
    idx_scan as scans_count,
    pg_size_pretty(pg_relation_size(indexrelid)) as index_size
FROM pg_stat_user_indexes
WHERE idx_scan < 50
ORDER BY idx_scan ASC, pg_relation_size(indexrelid) DESC;

SELECT 
    relname as "table", 
    seq_scan as full_scans, 
    idx_scan as index_scans, 
    pg_size_pretty(pg_relation_size(relid)) as table_size
FROM pg_stat_user_tables 
WHERE seq_scan > 100
ORDER BY seq_scan DESC 
LIMIT 10;

SELECT 
    relname as "table", 
    n_live_tup as live_rows, 
    n_dead_tup as dead_rows,
    round(n_dead_tup * 100.0 / nullif(n_live_tup + n_dead_tup, 0), 2) || '%' as dead_ratio,
    last_autovacuum as last_autovacuum_date
FROM pg_stat_user_tables
WHERE n_dead_tup > 100
ORDER BY n_dead_tup DESC;