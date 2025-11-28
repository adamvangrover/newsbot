const { useState, useEffect } = React;

function App() {
    const [activeComponent, setActiveComponent] = useState('home');
    const [reports, setReports] = useState([]);
    const [componentContent, setComponentContent] = useState('');
    const [error, setError] = useState(null);

    useEffect(() => {
        fetch('/reports')
            .then(response => {
                if (!response.ok) {
                    throw new Error('Failed to fetch reports');
                }
                return response.json();
            })
            .then(data => setReports(data))
            .catch(error => setError(error.message));
    }, []);

    const handleComponentClick = (componentId) => {
        setActiveComponent(componentId);
        setError(null);
        if (componentId.startsWith('report-')) {
            const reportName = componentId.substring(7);
            fetch(`/output/${reportName}`)
                .then(response => {
                    if (!response.ok) {
                        throw new Error(`Failed to fetch report: ${reportName}`);
                    }
                    return response.text();
                })
                .then(text => setComponentContent(text))
                .catch(error => setError(error.message));
        } else if (componentId === 'simulator') {
            setComponentContent(''); // Handled by specialized view
        } else if (componentId !== 'home') {
            fetch(`/components/${componentId}.md`)
                .then(response => {
                    if (!response.ok) {
                        // If generic component fetch fails, maybe it's just a view switch
                        if(componentId === 'simulator') return;
                        // For analysis etc, we might not have MD files yet, so ignore for now or handle
                        setComponentContent(`## ${componentId}\n\nContent placeholder.`);
                    }
                    return response.text();
                })
                .then(text => setComponentContent(text))
                .catch(error => {
                   // Fallback for missing MD
                   setComponentContent(`## ${componentId}\n\nContent placeholder (File not found).`);
                });
        }
    };

    return (
        <div className="catalog-container">
            <Sidebar
                activeComponent={activeComponent}
                setActiveComponent={handleComponentClick}
                reports={reports}
            />
            <div className="main-content">
                <Header component={activeComponent} />
                <div className="content-area">
                    {error && <ErrorMessage error={error} />}
                    {activeComponent === 'home' && <WelcomeScreen />}
                    {activeComponent === 'simulator' && <ScenarioSimulator />}
                    {activeComponent !== 'home' && activeComponent !== 'simulator' && <ComponentViewer content={componentContent} />}
                </div>
            </div>
        </div>
    );
}

function Sidebar({ activeComponent, setActiveComponent, reports }) {
    const [searchTerm, setSearchTerm] = useState('');

    const components = [
        { id: 'home', name: 'Home' },
        { id: 'simulator', name: 'Scenario Simulator' },
        { id: 'analysis', name: 'Analysis' },
        { id: 'federated_learning', name: 'Federated Learning' },
    ];

    const filteredComponents = components.filter(component =>
        component.name.toLowerCase().includes(searchTerm.toLowerCase())
    );

    const filteredReports = reports.filter(report =>
        report.toLowerCase().includes(searchTerm.toLowerCase())
    );

    return (
        <div className="sidebar">
            <div className="sidebar-header">
                <h2>NewsBot Nexus</h2>
            </div>
            <div className="sidebar-search">
                <input
                    type="text"
                    placeholder="Search..."
                    value={searchTerm}
                    onChange={e => setSearchTerm(e.target.value)}
                />
            </div>
            <nav className="sidebar-nav">
                <ul>
                    {filteredComponents.map(component => (
                        <li key={component.id} className={activeComponent === component.id ? 'active' : ''}>
                            <a href="#" onClick={() => setActiveComponent(component.id)}>{component.name}</a>
                        </li>
                    ))}
                    {filteredReports.length > 0 && <li className="separator">Reports</li>}
                    {filteredReports.map(report => (
                        <li key={`report-${report}`} className={activeComponent === `report-${report}` ? 'active' : ''}>
                            <a href="#" onClick={() => setActiveComponent(`report-${report}`)}>{report}</a>
                        </li>
                    ))}
                </ul>
            </nav>
        </div>
    );
}

function Header({ component }) {
    const titles = {
        home: 'Welcome',
        simulator: 'War Room: Scenario Simulator',
        analysis: 'Real-Time Analysis',
        federated_learning: 'Federated Learning',
    };

    const title = component.startsWith('report-') ? component.substring(7) : titles[component] || component;

    return (
        <header className="header">
            <div className="header-left">
                <h1>{title}</h1>
            </div>
        </header>
    );
}

function WelcomeScreen() {
    return (
        <div className="welcome-screen">
            <h1>NewsBot Nexus</h1>
            <p>Select a component from the sidebar.</p>
            <ul>
                <li><strong>Scenario Simulator:</strong> Run "what-if" simulations on the market.</li>
                <li><strong>Analysis:</strong> View real-time impact analysis (placeholder).</li>
            </ul>
        </div>
    );
}

function ComponentViewer({ content }) {
    const htmlContent = marked.parse(content || "");
    return (
        <div className="component-container" dangerouslySetInnerHTML={{ __html: htmlContent }} />
    );
}

function ScenarioSimulator() {
    const [scenarioName, setScenarioName] = useState("Custom Scenario");
    const [events, setEvents] = useState([
        { headline: "Fed raises rates by 0.5%", tickers_mentioned: ["SPY", "QQQ"] }
    ]);
    const [results, setResults] = useState(null);
    const [loading, setLoading] = useState(false);

    const addEvent = () => {
        setEvents([...events, { headline: "", tickers_mentioned: [] }]);
    };

    const updateEvent = (index, field, value) => {
        const newEvents = [...events];
        if (field === "tickers_mentioned") {
             // Split by comma
             newEvents[index][field] = value.split(",").map(s => s.trim());
        } else {
             newEvents[index][field] = value;
        }
        setEvents(newEvents);
    };

    const runSimulation = () => {
        setLoading(true);
        fetch('/api/reasoning/simulate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name: scenarioName, events: events })
        })
        .then(res => res.json())
        .then(data => {
            setResults(data);
            setLoading(false);
        })
        .catch(err => {
            console.error(err);
            setLoading(false);
        });
    };

    return (
        <div className="p-4">
            <div className="mb-4 p-4 border rounded bg-gray-50">
                <h3 className="text-lg font-bold mb-2">Configure Simulation</h3>
                <div className="mb-2">
                    <label className="block text-sm font-medium">Scenario Name</label>
                    <input
                        type="text"
                        value={scenarioName}
                        onChange={e => setScenarioName(e.target.value)}
                        className="border p-1 w-full"
                    />
                </div>
                <div className="space-y-2">
                    <label className="block text-sm font-medium">Events to Inject</label>
                    {events.map((ev, idx) => (
                        <div key={idx} className="flex gap-2">
                            <input
                                type="text"
                                placeholder="Headline (e.g. CEO Resigns)"
                                value={ev.headline}
                                onChange={e => updateEvent(idx, "headline", e.target.value)}
                                className="border p-1 flex-1"
                            />
                            <input
                                type="text"
                                placeholder="Tickers (comma sep)"
                                value={ev.tickers_mentioned.join(", ")}
                                onChange={e => updateEvent(idx, "tickers_mentioned", e.target.value)}
                                className="border p-1 w-1/3"
                            />
                        </div>
                    ))}
                    <button onClick={addEvent} className="text-sm text-blue-600">+ Add Event</button>
                </div>
                <button
                    onClick={runSimulation}
                    className="mt-4 bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
                    disabled={loading}
                >
                    {loading ? "Simulating..." : "Run Simulation"}
                </button>
            </div>

            {results && (
                <div className="mt-6">
                    <h3 className="text-xl font-bold mb-4">Simulation Results</h3>
                    <div className="space-y-4">
                        {results.outcomes.map((outcome, idx) => (
                            <div key={idx} className="border p-4 rounded shadow-sm bg-white">
                                <div className="flex justify-between items-start">
                                    <h4 className="font-semibold text-lg">{outcome.original_event}</h4>
                                    <span className={`px-2 py-1 rounded text-xs ${outcome.signal_strength === 'High Signal' ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'}`}>
                                        {outcome.signal_strength}
                                    </span>
                                </div>

                                {outcome.impact_chains.length > 0 ? (
                                    <div className="mt-3">
                                        <h5 className="text-sm font-medium text-gray-500 mb-2">Impact Chain:</h5>
                                        <ul className="space-y-2">
                                            {outcome.impact_chains.map((chain, cIdx) => (
                                                <li key={cIdx} className="text-sm border-l-2 border-blue-300 pl-3">
                                                    <div className="font-mono text-xs text-gray-400">{chain.logic_path}</div>
                                                    <div className="mt-1">
                                                        <span className="font-bold">{chain.impact_type}</span> on <span className="font-bold">{chain.target_entity}</span>
                                                        (Prob: {chain.probability})
                                                    </div>
                                                </li>
                                            ))}
                                        </ul>
                                    </div>
                                ) : (
                                    <p className="text-sm text-gray-500 mt-2">No direct impacts traced.</p>
                                )}
                            </div>
                        ))}
                    </div>
                </div>
            )}
        </div>
    );
}

function ErrorMessage({ error }) {
    return <div className="error-message">{error}</div>;
}

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<App />);
