from core.services.services import ViewBase


class SimpleView(ViewBase):

    def load_view(self, graph) -> str:
        result = self.create_script(graph)
        return result

    def identifier(self):
        return "1"

    def name(self):
        return "simpleView"

    def create_script(self, graph):
        result = "<script>"

        result += self.create_nodes(graph)

        result += self.create_links(graph)

        result += self.create_force_layout()

        result += self.create_d3_objects(graph)

        result += self.create_function_simple_view()

        result += self.create_function_tick()

        result += self.create_zoom_function()

        result += self.createNodeClickFunction(graph)

        result += "</script>"

        return result

    def createNodeClickFunction(self, graph):

        result = "\n" \
                 "function nodeClick(vertex){\n" \
                 "var node = nodes[vertex.id];" \
                 "console.log( node );" \
                 "poruka = '';" \
                 "poruka += vertex.id+'\\n';" \
                 "\n" \
                 "for (const [key, value] of Object.entries(node.attributes)) {\n" \
                 "poruka += String(key).toUpperCase() +' : '+ String(value).toUpperCase() + '\\n';\n" \
                 "}" \
                 "alert(poruka);\n" \
                 "id = vertex.id.split('_')[1];" \
                 "console.log('id select simple view :' + id);" \
                 "selectVertex(id);" \
                 "}\n"

        return result

    def create_nodes(self, graph):
        result = "let nodes= {"
        for cvor in graph.vertices():
            result += "'cvor_" + str(cvor.Id) + "':{" \
                                                "name:'cvor_" + str(cvor.Id) + "'," \
                                                                               "id:" + str(cvor.Id) + \
                      ",attributes:{"
            for k, v in cvor.attributes.items():
                result += "'" + str(k).replace("'", '').replace('"', "") + "': '" + str(v).replace("'", '').replace('"',
                                                                                                                    "") + "',"

            result += "'':''}},"
        result += "};\n"
        return result

    def create_links(self, graph):
        result = "let links=["
        for cvor in graph.vertices():
            for komsija in cvor.neighbors:
                result += "{ source:'cvor_" + str(cvor.Id) + "'," \
                                                             "target:'cvor_" + str(komsija.Id) + "'" + \
                          "},"
        result += "];\n"

        result += "links.forEach(function(link) {" \
                  "link.source = nodes[link.source];" \
                  "link.target = nodes[link.target];" \
                  "});\n"

        return result

    def create_force_layout(self):
        result = 'let sirinaMainPlatna = parseInt(d3.select("#svgMain").style("width"),10);' \
                 'let visinaMainPlatna = parseInt(d3.select("#svgMain").style("height"),10);' \
                 "" \
                 "var force = d3.layout.force() // kreiranje force layout-a\n" \
                 ".size([sirinaMainPlatna, visinaMainPlatna]) // raspoloziv prostor za iscrtavanje\n" \
                 ".nodes(d3.values(nodes)) // dodavanje informacija o cvorovima grafa\n" \
                 ".links(links) // dodavanje informacije o ivicama grafa\n" \
                 ".on('tick', tick) // Dogadjaj tick okida se prilikokm svakog koraka simulacije.\n" \
                 ".linkDistance(100) // duzina ivice grafa\n" \
                 ".charge(-100) // koliko da se elementi odbijaju (pozitivna vrednost kaze koliko se elementi " \
                 "privlace)\n" \
                 ".start(); //pokreni simulaciju\n"
        return result

    def create_d3_objects(self, graph):
        result = "var zoomMain = d3.behavior" \
                 ".zoom()" \
                 ".scaleExtent([1/10, 4])" \
                 ".on('zoom.zoom', function () {" \
                 "root.attr('transform'," \
                 "'translate(' + d3.event.translate + ')'" \
                 "	+   'scale(' + d3.event.scale     + ')');" \
                 "" \
                 "bird.attr('transform'," \
                 "                   'translate('+ " \
                 "                    (-bw_scale_faktor * d3.event.translate[0])/d3.event.scale+" \
                 "					','+" \
                 "							(-bw_scale_faktor * d3.event.translate[1])/d3.event.scale+" \
                 "					')'+" \
                 "							'scale('+" \
                 "							bw_scale_faktor / d3.event.scale +')');" \
                 "})" \
                 ';\n' \
                 "br_cvorova = " + str(len(graph.vertices())) + " ;" \
                                                                "if(br_cvorova > 10)" \
                                                                "bw_scale_faktor = 0.2 - 0.5 / br_cvorova ;  \n" \
                                                                "else bw_scale_faktor = 0.2 ; \n" \
                                                                "console.log(bw_scale_faktor);" \
                                                                "var svg=d3.select('#svgMain')" \
                                                                "				.call(zoomMain);" \
                                                                "" \
                                                                "var bird = svg.select('#bird_view');\n" \
                                                                "var root = svg.select('#rootMain');\n" \
                                                                "var nodes_groupMain = root.select('#nodesMain');\n" \
                                                                "var links_groupMain = root.select('#linksMain');\n"

        result += "var link = links_groupMain.selectAll('.link')" \
                  ".data(links)" \
                  ".enter().append('line')" \
                  ".attr('class', 'link')" \
                  '.attr("stroke","#031554");\n'

        result += "var node = nodes_groupMain.selectAll('.node')" \
                  ".data(force.nodes()) " \
                  ".enter().append('g')" \
                  ".attr('class', 'node')" \
                  ".attr('id', function(d){return d.name;})" \
                  ".on('click',function(){ nodeClick(this);})" \
                  ".call(force" \
                  ".drag()" \
                  ".on('dragstart', function() {" \
                  "d3.event.sourceEvent.stopPropagation();" \
                  "})" \
                  ");;\n"

        result += "node.each(function(d){simpleView(d);});\n"

        return result

    def create_function_simple_view(self):

        result = "function simpleView(d){" \
                 "var duzina=50;" \
                 "var textSize=10;" \
                 "var visina=50;" \
                 'd3.select("g#"+d.name)' \
                 ".append('circle')" \
                 ".attr('x',0)" \
                 ".attr('r',10)" \
                 ".attr('y',0)" \
                 ".attr('fill','url(#gradientVertex)')" \
                 "\n" \
                 'd3.select("g#"+d.name)' \
                 ".append('circle')" \
                 ".attr('x',0)" \
                 ".attr('r',10)" \
                 ".attr('y',0)" \
                 ".attr('fill','url(#gradientVertex2)')" \
                 "\n" \
                 'd3.select("g#"+d.name)' \
                 ".append('text')" \
                 ".attr('x',duzina/2)" \
                 ".attr('y',10)" \
                 ".attr('text-anchor','middle')" \
                 ".attr('font-size',textSize)" \
                 ".attr('font-family','sans-serif')" \
                 ".attr('fill','green')" \
                 ".text(d.id);\n" \
                 "}\n"
        return result

    def create_function_tick(self):
        result = "function tick(e) {" \
                 "node.attr('transform', function(d) {" \
                 'return "translate(" + d.x + "," + d.y + ")";' \
                 "})" \
                 ".call(force.drag);" \
                 "link.attr('x1', function(d) { return d.source.x; })" \
                 "    .attr('y1', function(d) { return d.source.y; })" \
                 "    .attr('x2', function(d) { return d.target.x; })" \
                 "    .attr('y2', function(d) { return d.target.y; });" \
                 "}"
        return result

    def create_zoom_function(self):
        result = "lapsedZoomFit(500,0);\n" \
                 "" \
                 "" \
                 "function lapsedZoomFit(ticks, transitionDuration) {" \
                 " for (var i = ticks || 200; i > 0; --i) force.tick();" \
                 "force.stop();" \
                 "zoomFit(0.5, transitionDuration);" \
                 "}\n" \
                 "function zoomFit(paddingPercent, transitionDuration) {" \
                 "var bounds = root.node().getBBox();" \
                 "var parent = root.node().parentElement;" \
                 "var fullWidth = parent.clientWidth," \
                 "fullHeight = parent.clientHeight;" \
                 "var width = bounds.width," \
                 "height = bounds.height;" \
                 "var midX = bounds.x + width / 2," \
                 "midY = bounds.y + height / 2;" \
                 "if (width == 0 || height == 0) return; // nothing to fit\n" \
                 "var scale = (paddingPercent || 0.75) / Math.max(width / fullWidth, height / fullHeight);" \
                 "var translate = [fullWidth / 2 - scale * midX, fullHeight / 2 - scale * midY];\n" \
                 "root" \
                 ".transition()" \
                 ".duration(transitionDuration || 0) // milliseconds\n" \
                 ".call(zoomMain.translate(translate).scale(scale).event);" \
                 "}\n"

        return result
