from core.services.services import ViewBase


class AdvancedView(ViewBase):

    def get_id(self):
        return "2"

    def get_name(self):
        return "advancedView"

    def render_view(self, graph) -> str:
        script_content = "<script>"
        script_content += self.build_node_dict(graph)
        script_content += self.build_links(graph)
        script_content += self.setup_force_layout()
        script_content += self.setup_d3_elements(graph)
        script_content += self.render_advanced_view()
        script_content += self.handle_tick_event()
        script_content += self.initialize_zoom()
        script_content += self.node_click_handler()
        script_content += "</script>"

        return script_content

    def build_node_dict(self, graph):
        node_string = "var nodeData = {"
        for vertex in graph.vertices():
            node_id = "'node_" + str(vertex.Id) + "'"
            node_string += node_id + ":{id:" + node_id + ", label:'" + str(vertex.name) + "',"
            for attribute, value in vertex.attributes.items():
                sanitized_value = str(value).replace("'", "").replace(",", "").replace('"', "")
                if len(sanitized_value) > 20:
                    sanitized_value = sanitized_value[:20]
                node_string += f"{attribute}:'{sanitized_value}',"
            node_string += "},"
        node_string += '};\n'
        return node_string

    def build_links(self, graph):
        link_string = "var linkData = ["
        for vertex in graph.vertices():
            for neighbor in vertex.neighbors:
                link_string += "{src: 'node_" + str(vertex.Id) + "', tgt: 'node_" + str(neighbor.Id) + "'},"
        link_string += "];\n"
        link_string += """
            linkData.forEach(function(link) {
                link.src = nodeData[link.src];
                link.tgt = nodeData[link.tgt];
            });\n"""
        return link_string

    def setup_force_layout(self):
        layout = """
            var force = d3.layout.force()
                .size([400, 400])
                .nodes(d3.values(nodeData))
                .links(linkData)
                .on('tick', tickEvent)
                .linkDistance(500)
                .charge(-100)
                .start();
        """
        return layout

    def setup_d3_elements(self, graph):
        d3_code = """
            var zoomBehavior = d3.behavior.zoom()
                .scaleExtent([0.1, 4])
                .on('zoom', function () {
                    container.attr('transform', 
                        'translate(' + d3.event.translate + ') scale(' + d3.event.scale + ')');
                });
            
            let node_count = """ + str(len(graph.vertices())) + """;
            let scale_factor = node_count > 5 ? 0.2 - 0.5 / node_count : 0.2;
            console.log(scale_factor);

            var svgCanvas = d3.select('#mainCanvas').call(zoomBehavior);
            var container = svgCanvas.select('#mainGroup');
            var nodeGroup = container.select('#nodeGroup');
            var linkGroup = container.select('#linkGroup');
            
            var link = linkGroup.selectAll('.link')
                .data(linkData)
                .enter().append('line')
                .attr('class', 'link')
                .attr('stroke', '#031554');

            var node = nodeGroup.selectAll('.node')
                .data(force.nodes())
                .enter().append('g')
                .attr('class', 'node')
                .attr('id', function(d){ return d.id; })
                .on('click', function(){ handleClick(this); })
                .call(force.drag().on('dragstart', function() {
                    d3.event.sourceEvent.stopPropagation();
                }));

            node.each(function(d){ renderAdvancedView(d); });
        """
        return d3_code

    def render_advanced_view(self):

        view_function = """
            function renderAdvancedView(d) {
                var rect_width = 150;
                var attr_count = Object.keys(nodeData[d.id]).length;
                var text_height = 10;
                var rect_height = attr_count <= 6 ? text_height : (attr_count - 6) * text_height + 3;
                rect_height += text_height;
                
                d3.select('g#' + d.id)
                    .append('rect')
                    .attr('x', 0)
                    .attr('y', 0)
                    .attr('width', rect_width)
                    .attr('height', rect_height)
                    .attr('fill', 'white');
                
                d3.select('g#' + d.id)
                    .append('text')
                    .attr('x', rect_height / 2)
                    .attr('y', 10)
                    .attr('text-anchor', 'middle')
                    .attr('font-size', text_height)
                    .attr('font-family', 'sans-serif')
                    .attr('fill', 'black')
                    .text(d.label);
                
                d3.select('g#' + d.id)
                    .append('line')
                    .attr('x1', 0)
                    .attr('y1', text_height + 3)
                    .attr('x2', rect_width)
                    .attr('y2', text_height + 3)
                    .attr('stroke', 'green')
                    .attr('stroke-width', 2);

                var attributes = nodeData[d.id];
                var remove_list = ['index', 'px', 'py', 'x', 'y', 'weight', 'label', 'id'];
                var i = 0;
                
                for (var attribute in attributes) {
                    if (!remove_list.includes(attribute)) {
                        d3.select('g#' + d.id)
                            .append('text')
                            .attr('x', 0)
                            .attr('y', 20 + i * text_height)
                            .attr('text-anchor', 'start')
                            .attr('font-size', text_height)
                            .attr('font-family', 'sans-serif')
                            .attr('fill', 'black')
                            .text(attribute + ': ' + attributes[attribute]);
                        i++;
                    }
                }
            }
        """
        return view_function

    def handle_tick_event(self):
        tick_function = """
            function tickEvent() {
                node.attr('transform', function(d) {
                    return 'translate(' + d.x + ',' + d.y + ')';
                }).call(force.drag);

                link.attr('x1', function(d) { return d.src.x; })
                    .attr('y1', function(d) { return d.src.y; })
                    .attr('x2', function(d) { return d.tgt.x; })
                    .attr('y2', function(d) { return d.tgt.y; });
            }
        """
        return tick_function

    def initialize_zoom(self):
        zoom_code = """
            fitToBounds(500, 0);

            function fitToBounds(ticks, transitionDuration) {
                for (var i = ticks || 200; i > 0; --i) force.tick();
                force.stop();
                zoomToFit(0.5, transitionDuration);
            }

            function zoomToFit(paddingPercent, transitionDuration) {
                var bounds = container.node().getBBox();
                var parentEl = container.node().parentElement;
                var fullWidth = parentEl.clientWidth;
                var fullHeight = parentEl.clientHeight;
                var width = bounds.width;
                var height = bounds.height;
                var midX = bounds.x + width / 2;
                var midY = bounds.y + height / 2;

                if (width === 0 || height === 0) return;

                var scale = (paddingPercent || 0.75) / Math.max(width / fullWidth, height / fullHeight);
                var translate = [fullWidth / 2 - scale * midX, fullHeight / 2 - scale * midY];

                container.transition().duration(transitionDuration || 0)
                    .call(zoomBehavior.translate(translate).scale(scale).event);
            }
        """
        return zoom_code

    def node_click_handler(self):
        click_function = """
            function handleClick(node) {
                var nodeAttributes = nodeData[node.id];
                var message = node.id + '\\n';
                
                for (var attribute in nodeAttributes) {
                    message += attribute.toUpperCase() + ': ' + String(nodeAttributes[attribute]).toUpperCase() + '\\n';
                }

                alert(message);
                selectVertex(node.id.slice(5));
            }
        """
        return click_function
