{% macro drop_schema_by_name (schema_name) %}

    {% set query %}
        drop schema if exists "{{ schema_name }}" cascade
    {% endset %}

    {% do run_query(query) %}

{% endmacro %}
