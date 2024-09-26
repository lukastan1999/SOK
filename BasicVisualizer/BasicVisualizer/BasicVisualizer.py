from core.services.services import ViewBase

class BasicVisualizer(ViewBase):

    def load_view(self, graph) -> str:
        visualization_script = self._generate_script(graph)
        return visualization_script

    def identifier(self):
        return "1"

    def name(self):
        return "basicView"

    def _generate_script(self, graph):
        script = "<script>"

        script += self._generate_nodes(graph)
        script += self._generate_edges(graph)
        script += self._initialize_force_layout()
        script += self._set_d3_objects(graph)
        script += self._simple_view_function()
        script += self._tick_function()
        script += self._zoom_function()
        script += self._on_node_click_function(graph)

        script += "</script>"

        return script

    def _on_node_click_function(self, graph):
        script = "\n" \
                 "function handleNodeClick(vertex) {\n" \
                 "let selectedNode = nodes[vertex.id];" \
                 "console.log(selectedNode);" \
                 "let details = '';" \
                 "details += vertex.id + '\\n';" \
                 "\n" \
                 "for (const [key, value] of Object.entries(selectedNode.attributes)) {\n" \
                 "details += String(key).toUpperCase() + ': ' + String(value).toUpperCase() + '\\n';\n" \
                 "}" \
                 "alert(details);\n" \
                 "let idPart = vertex.id.split('_')[1];" \
                 "console.log('Selected ID: ' + idPart);" \
                 "selectVertex(idPart);" \
                 "}\n"
        return script

    def _generate_nodes(self, graph):
        script = "let nodes = {"
        for vertex in graph.vertices():
            script += "'node_" + str(vertex.Id) + "': {" \
                                                  "name: 'node_" + str(vertex.Id) + "'," \
                                                  "id: " + str(vertex.Id) + "," \
                                                  "attributes: {"
            for k, v in vertex.attributes.items():
                script += "'" + str(k).replace("'", '').replace('"', "") + "': '" + str(v).replace("'", '').replace('"', "") + "',"
            script += "'':''}},"
        script += "};\n"
        return script

    def _generate_edges(self, graph):
        script = "let edges = ["
        for vertex in graph.vertices():
            for neighbor in vertex.neighbors:
                script += "{ source: 'node_" + str(vertex.Id) + "'," \
                          "target: 'node_" + str(neighbor.Id) + "'},"
        script += "];\n"

        script += "edges.forEach(function(edge) {" \
                  "edge.source = nodes[edge.source];" \
                  "edge.target = nodes[edge.target];" \
                  "});\n"

        return script

    def _initialize_force_layout(self):
        script = 'let canvasWidth = parseInt(d3.select("#svgMain").style("width"), 10);' \
                 'let canvasHeight = parseInt(d3.select("#svgMain").style("height"), 10);' \
                 "" \
                 "var forceLayout = d3.layout.force()" \
                 ".size([canvasWidth, canvasHeight])" \
                 ".nodes(d3.values(nodes))" \
                 ".links(edges)" \
                 ".on('tick', tick)" \
                 ".linkDistance(100)" \
                 ".charge(-100)" \
                 ".start();\n"
        return script

    def _set_d3_objects(self, graph):
        script = "let zoomBehavior = d3.behavior.zoom().scaleExtent([1/10, 4]).on('zoom', function () {" \
                 "svgRoot.attr('transform', 'translate(' + d3.event.translate + ')' + 'scale(' + d3.event.scale + ')');" \
                 "birdView.attr('transform', 'translate(' + (-scaleFactor * d3.event.translate[0]) / d3.event.scale + ',' + (-scaleFactor * d3.event.translate[1]) / d3.event.scale + ') scale(' + scaleFactor / d3.event.scale + ');');" \
                 "});\n"

        script += "let nodeCount = " + str(len(graph.vertices())) + ";" \
                  "scaleFactor = (nodeCount > 10) ? 0.2 - 0.5 / nodeCount : 0.2;" \
                  "console.log(scaleFactor);\n"

        script += "let svg = d3.select('#svgMain').call(zoomBehavior);" \
                  "let birdView = svg.select('#bird_view');\n" \
                  "let svgRoot = svg.select('#rootMain');\n" \
                  "let nodeGroup = svgRoot.select('#nodesMain');\n" \
                  "let linkGroup = svgRoot.select('#linksMain');\n"

        script += "let linkElements = linkGroup.selectAll('.link')" \
                  ".data(edges)" \
                  ".enter().append('line')" \
                  ".attr('class', 'link')" \
                  '.attr("stroke", "#031554");\n'

        script += "let nodeElements = nodeGroup.selectAll('.node')" \
                  ".data(forceLayout.nodes())" \
                  ".enter().append('g')" \
                  ".attr('class', 'node')" \
                  ".attr('id', function(d){ return d.name; })" \
                  ".on('click', function(){ handleNodeClick(this); })" \
                  ".call(forceLayout.drag().on('dragstart', function() { d3.event.sourceEvent.stopPropagation(); }));\n"

        script += "nodeElements.each(function(d){ visualizeNode(d); });\n"

        return script

    def _simple_view_function(self):
        script = "function visualizeNode(d){" \
                 "let circleRadius = 10;" \
                 'd3.select("g#"+d.name)' \
                 ".append('circle')" \
                 ".attr('r', circleRadius)" \
                 ".attr('fill', 'url(#gradientVertex)');" \
                 "\n" \
                 'd3.select("g#"+d.name)' \
                 ".append('text')" \
                 ".attr('x', 25)" \
                 ".attr('y', 10)" \
                 ".attr('text-anchor', 'middle')" \
                 ".attr('font-size', 10)" \
                 ".attr('font-family', 'sans-serif')" \
                 ".attr('fill', 'green')" \
                 ".text(d.id);\n" \
                 "}\n"
        return script

    def _tick_function(self):
        script = "function tick() {" \
                 "nodeElements.attr('transform', function(d) { return 'translate(' + d.x + ',' + d.y + ')'; })" \
                 ".call(forceLayout.drag);" \
                 "linkElements.attr('x1', function(d) { return d.source.x; })" \
                 "    .attr('y1', function(d) { return d.source.y; })" \
                 "    .attr('x2', function(d) { return d.target.x; })" \
                 "    .attr('y2', function(d) { return d.target.y; });" \
                 "}\n"
        return script

    def _zoom_function(self):
        script = "fitZoomToCanvas(500, 0);\n" \
                 "function fitZoomToCanvas(ticks, duration) {" \
                 "for (let i = ticks || 200; i > 0; --i) forceLayout.tick();" \
                 "forceLayout.stop();" \
                 "applyZoomFit(0.5, duration);" \
                 "}\n" \
                 "function applyZoomFit(paddingPercent, duration) {" \
                 "let bounds = svgRoot.node().getBBox();" \
                 "let parent = svgRoot.node().parentElement;" \
                 "let widthFull = parent.clientWidth, heightFull = parent.clientHeight;" \
                 "let boxWidth = bounds.width, boxHeight = bounds.height;" \
                 "let midX = bounds.x + boxWidth / 2, midY = bounds.y + boxHeight / 2;" \
                 "if (boxWidth == 0 || boxHeight == 0) return;" \
                 "let zoomScale = (paddingPercent || 0.75) / Math.max(boxWidth / widthFull, boxHeight / heightFull);" \
                 "let translatePosition = [widthFull / 2 - zoomScale * midX, heightFull / 2 - zoomScale * midY];" \
                 "svgRoot.transition().duration(duration || 0).call(zoomBehavior.translate(translatePosition).scale(zoomScale).event);" \
                 "}\n"
        return script
