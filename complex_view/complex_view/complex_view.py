from core.services.services import ViewBase


class ComplexView(ViewBase):

    def identifier(self):
        return "2"

    def name(self):
        return "complexView"

    def load_view(self, graph) -> str:
        view = "<script>"
        view += self.create_dict_vertices_attributes(graph)
        view += self.create_edges(graph)
        view += self.force_layout()
        view += self.d3_objects(graph)
        view += self.complexView()
        view += self.tick()
        view += self.create_zoom_function()
        view += self.select_node()
        view += "</script>"

        return view

    def create_dict_vertices_attributes(self, graph):
        nodes = "var nodes = {"
        for v in graph.vertices():
            nodes += "'cvor" + str(v.Id) + "'"
            nodes += ":"
            nodes += "{id:'cvor" + str(v.Id) +"', name:'" + str(v.name) + "',"
            for atr in v.attributes:

                value = str(v.attributes[atr])
                value = value.replace("'","")
                value = value.replace(",","")
                value = value.replace("\"","")
                if len(value) > 20:
                    value = value[:20]
                nodes += str(atr) + ":'" + value + "',"
            nodes += "},"
        nodes += '};\n'
        return nodes

    def create_edges(self, graph):
        links = "var links=["
        for v in graph.vertices():
            for n in v.neighbors:
                links += "{source: 'cvor" + str(v.Id) + "',target:'cvor" + str(n.Id) + "'},"
        links += "];\n"

        links += "links.forEach(function(link) {" \
                 "link.source = nodes[link.source];" \
                 "link.target = nodes[link.target];" \
                 "});\n"

        return links

    def force_layout(self):
        force = "var force = d3.layout.force()" \
                ".size([400, 400])" \
                ".nodes(d3.values(nodes))" \
                ".links(links)" \
                ".on('tick', tick)" \
                ".linkDistance(500)" \
                ".charge(-100)" \
                ".start();"
        return force

    def d3_objects(self,graph):
        d3 = "var zoomMain = d3.behavior" \
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
                 "br_cvorova = "+str(len(graph.vertices()))+" ;" \
                 "if(br_cvorova > 5)" \
                 "bw_scale_faktor = 0.2 - 0.5 / br_cvorova ;  \n" \
                 "else bw_scale_faktor = 0.2 ; \n" \
                 "console.log(bw_scale_faktor);" \
                 "var svg=d3.select('#svgMain')" \
                 "				.call(zoomMain);" \
                 "var bird = svg.select('#bird_view');\n" \
                 "var root = svg.select('#rootMain');\n" \
                 "var nodes_groupMain = root.select('#nodesMain');\n" \
                 "var links_groupMain = root.select('#linksMain');\n"\
             "var link = links_groupMain.selectAll('.link')" \
                  ".data(links)" \
                  ".enter().append('line')" \
                  ".attr('class', 'link')" \
                  '.attr("stroke","#031554");\n'\
             "var node = nodes_groupMain.selectAll('.node')" \
                  ".data(force.nodes()) " \
                  ".enter().append('g')" \
                  ".attr('class', 'node')" \
                  ".attr('id', function(d){return d.id;})" \
                  ".on('click',function(){ nodeClick(this);})" \
                  ".call(force" \
                  ".drag()" \
                  ".on('dragstart', function() {" \
                  "d3.event.sourceEvent.stopPropagation();" \
                  "})" \
                  ");;\n"\
             "node.each(function(d){complexView(d);});" \
             "function zoom() {" \
             "var zoom = d3.event;" \
             "svg.attr('transform', 'translate(' + zoom.translate + ')scale(' + zoom.scale + ')');}"
        return d3

    def complexView(self):

        func = "function complexView(d){" \
               "var width=150;" \
               "var attrNumber=Object.keys(nodes[d.id]).length;" \
               "var textSize=10;"\
               "var height=(attrNumber==0)?textSize:(attrNumber-6)*textSize+3;" \
               "height+=textSize;" \
               " d3.select('g#'+d.id)" \
               ".append('rect')" \
               ".attr('x',0).attr('y',0).attr('width',width).attr('height',height)" \
               ".attr('fill','white');" \
               " d3.select('g#'+d.id).append('text').attr('x',height/2).attr('y',10)" \
               ".attr('text-anchor','middle')" \
               ".attr('font-size',textSize).attr('font-family','sans-serif')" \
               ".attr('fill','black').text(d.name);" \
               " d3.select('g#'+d.id).append('line')" \
               ".attr('x1',0).attr('y1',textSize+3).attr('x2',width).attr('y2',textSize+3)" \
               ".attr('stroke','green').attr('stroke-width',2);" \
               "var attributes = nodes[d.id];" \
               "" \
               "var i=0;" \
               "const for_remove = ['index','px','py','x','y','weight','name','id'];" \
               "for(var attr in attributes){" \
               "if(!for_remove.includes(attr)){" \
               "d3.select('g#'+d.id).append('text').attr('x',0).attr('y',20+i*textSize)" \
               ".attr('text-anchor','start')" \
               ".attr('font-size',textSize).attr('font-family','sans-serif')" \
               ".attr('fill','black').text(attr + ':' + attributes[attr]);" \
               "i++;} " \
               "}}\n"
        return func

    def tick(self):
        tick = "function tick(e) {" \
               "node.attr('transform', function(d) " \
               "{return 'translate(' + d.x + ',' + d.y + ')';}).call(force.drag);" \
               "link.attr('x1', function(d) { return d.source.x; })" \
               ".attr('y1', function(d) { return d.source.y; })" \
               ".attr('x2', function(d) { return d.target.x; })" \
               ".attr('y2', function(d) { return d.target.y; });}"
        return tick

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
                 "}"

        return result

    def select_node(self):

        result = "\n" \
                 "function nodeClick(node){\n" \
                 "var attributes = nodes[node.id];" \
                 "console.log(attributes);" \
                 "poruka = '';" \
                 "poruka += node.id\n;" \
                 "\n" \
                 "for (var atr in attributes) {\n" \
                 "poruka += String(atr).toUpperCase() +' : '+ String(attributes[atr]).toUpperCase() + '\\n';\n" \
                 "}" \
                 "alert(poruka);\n" \
                 "selectVertex(node.id.slice(4));" \
                 "}"

        return result