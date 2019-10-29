var data = {{ object.data|safe }};
var labels = {{ object.labels|safe }};
{% for template in object.templates.all %}
    ngraph = new RGraph.SVG.Bar({
        id: 'chart-{{ template.uid }}',
        data: data,
        options: {
            {% if 'title' in object.options %}
            title: {{ object.options.title|lower|safe }},
            {% else %}
            title: '{{ object.title }}',
            {% endif %}
            xaxisLabels: labels,
            {% if template.options %}
            {% for key,value in template.options.items %}
            {% if key not in object.options %}{{ key }}: {{ value|lower|safe }},{% endif %}
            {% endfor %}
            {% endif %}
            {% if object.options %}
            {% for key,value in object.options.items %}
            {{ key }}: {{ value|lower|safe }},
            {% endfor %}
            {% endif %}
        },
    });

    {% if object.is_responsive %}
    ngraph.draw().responsive([
        {
            maxWidth: {{ template.sm_max_width }}, 
            width: {{ template.sm_width }},
            height: {{ template.sm_height }},
                options: {
                    titleSize: {{ template.sm_title_size }},
                    textSize: {{ template.sm_text_size }},
                    {% if template.responsive_options and template.responsive_options.lg %}
                    {% for key,value in template.responsive_options.lg.items %}
                    {% if key not in object.responsive_options.lg %}{{ key }}: {{ value|lower|safe }},{% endif %}
                    {% endfor %}
                    {% endif %}
                    {% if object.responsive_options.lg %}
                    {% for key,value in object.responsive_options.lg.items %}
                    {{ key }}: {{ value|lower|safe }},
                    {% endfor %}
                    {% endif %}
                },
        },
        {
            maxWidth: {{ template.md_max_width }}, 
            width: {{ template.md_width }},
            height: {{ template.md_height }},
                options: {
                    titleSize: {{ template.md_title_size }},
                    textSize: {{ template.md_text_size }},
                    {% if template.responsive_options and template.responsive_options.md %}
                    {% for key,value in template.responsive_options.md.items %}
                    {% if key not in object.responsive_options.md %}{{ key }}: {{ value|lower|safe }},{% endif %}
                    {% endfor %}
                    {% endif %}
                    {% if object.responsive_options.md %}
                    {% for key,value in object.responsive_options.md.items %}
                    {{ key }}: {{ value|lower|safe }},
                    {% endfor %}
                    {% endif %}
                },
        },
        {
            maxWidth: null, 
            width: {{ template.lg_width }},
            height: {{ template.lg_height }},
                options: {
                    titleSize: {{ template.lg_title_size }},
                    textSize: {{ template.lg_text_size }},
                    {% if template.responsive_options and template.responsive_options.sm %}
                    {% for key,value in template.responsive_options.sm.items %}
                    {% if key not in object.responsive_options.sm %}{{ key }}: {{ value|lower|safe }},{% endif %}
                    {% endfor %}
                    {% endif %}
                    {% if object.responsive_options.sm %}
                    {% for key,value in object.responsive_options.sm.items %}
                    {{ key }}: {{ value|lower|safe }},
                    {% endfor %}
                    {% endif %}
                },
        },
    ]);
    {% else %}
    ngraph.draw();
    {% endif %}
{% endfor %}