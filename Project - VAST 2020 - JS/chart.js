d3.csv("Data/CGCS-Template.csv").then(function (data) {

    var nodes = [];
    var links = [];

    data.forEach(function (d) {

        var sourceNode = nodes.find(node => node.id === d.Source);
        var targetNode = nodes.find(node => node.id === d.Target);

        if (!sourceNode) {
            sourceNode = { id: d.Source };
            nodes.push(sourceNode);
        }

        if (!targetNode) {
            targetNode = { id: d.Target };
            nodes.push(targetNode);
        }

        links.push({ source: sourceNode, target: targetNode });
    });

    var simulation = d3.forceSimulation(nodes)
        .force("link", d3.forceLink(links).id(d => d.id))
        .force("charge", d3.forceManyBody())
        .force("center", d3.forceCenter(850, 450));

    var svg = d3.select("svg");

    var link = svg.selectAll(".link")
        .data(links)
        .enter().append("line")
        .attr("class", "link");

    var node = svg.selectAll(".node")
        .data(nodes)
        .enter().append("circle")
        .attr("class", "node")
        .attr("r", 5);


    simulation.on("tick", function () {
        link
            .attr('x1', d => d.source.x)
            .attr('y1', d => d.source.y)
            .attr('x2', d => d.target.x)
            .attr('y2', d => d.target.y)
            .attr('stroke-width', 1)
            .attr('stroke', 'red');

        node
            .attr("cx", d => d.x)
            .attr("cy", d => d.y);
    });
});
