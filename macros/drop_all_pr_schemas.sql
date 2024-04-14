{% macro drop_all_pr_schemas () %}

    {% set query %}
        select distinct table_schema from information_schema.tables where table_schema like 'pr\_\_%'
    {% endset %}

    {% set pr_schemas = run_query(query) %}

    {% for schema_info in pr_schemas %}
        {{ drop_schema_by_name(schema_info[0]) }}
    {% endfor %}

{% endmacro %}