{% if template.options %}
{% for key,value in template.options.items %}
{% if key not in object.options or not object.options %}{{ key }}: {{ value|lower|safe }},{% endif %}
{% endfor %}
{% endif %}
{% if object.options %}
{% for key,value in object.options.items %}
{{ key }}: {{ value|lower|safe }},
{% endfor %}
{% endif %}
{% if object.bar_values.options %}
{% for key,value in object.bar_values.options.items %}
{{ key }}: {{ value|lower|safe }},
{% endfor %}
{% endif %}