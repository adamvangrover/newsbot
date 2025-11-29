import React, { useRef } from 'react';
import ForceGraph2D, { type ForceGraphMethods } from 'react-force-graph-2d';

const ImpactGraph: React.FC = () => {
    // Correctly type the ref
    const fgRef = useRef<ForceGraphMethods | undefined>(undefined);

    // Mock Data representing Impact Chains
    const data = {
        nodes: [
            { id: "Event: Rate Hike", group: 1, val: 20 },
            { id: "Tech Sector", group: 2, val: 10 },
            { id: "Real Estate", group: 2, val: 10 },
            { id: "Company A", group: 3, val: 5 },
            { id: "Company B", group: 3, val: 5 },
            { id: "Consumer Discretionary", group: 2, val: 8 },
        ],
        links: [
            { source: "Event: Rate Hike", target: "Tech Sector", type: "Negative" },
            { source: "Event: Rate Hike", target: "Real Estate", type: "Negative" },
            { source: "Tech Sector", target: "Company A", type: "Down" },
            { source: "Tech Sector", target: "Company B", type: "Down" },
            { source: "Event: Rate Hike", target: "Consumer Discretionary", type: "Negative" },
        ]
    };

    return (
        <div className="bg-gray-900 border border-gray-700 rounded h-96 overflow-hidden relative">
             <div className="absolute top-2 left-2 text-white font-mono z-10 bg-black bg-opacity-50 px-2 rounded">
                Impact Graph (Force Directed)
            </div>
            <ForceGraph2D
                ref={fgRef}
                graphData={data}
                nodeLabel="id"
                nodeColor={(node: any) => {
                    if (node.group === 1) return "red";
                    if (node.group === 2) return "orange";
                    return "yellow";
                }}
                linkColor={() => "rgba(255,255,255,0.2)"}
                backgroundColor="#111"
                width={800} // ideally responsive
                height={380}
            />
        </div>
    );
};

export default ImpactGraph;
