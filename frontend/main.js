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
        } else if (componentId !== 'home') {
            fetch(`/components/${componentId}.md`)
                .then(response => {
                    if (!response.ok) {
                        throw new Error(`Failed to fetch component: ${componentId}`);
                    }
                    return response.text();
                })
                .then(text => setComponentContent(text))
                .catch(error => setError(error.message));
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
                    {activeComponent !== 'home' && <ComponentViewer content={componentContent} />}
                </div>
            </div>
        </div>
    );
}

function Sidebar({ activeComponent, setActiveComponent, reports }) {
    const [searchTerm, setSearchTerm] = useState('');

    const components = [
        { id: 'home', name: 'Home' },
        { id: 'analysis', name: 'Analysis' },
        { id: 'clustering_techniques', name: 'Clustering Techniques' },
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
                <h2>Repo Catalog</h2>
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
        analysis: 'Real-Time Analysis',
        clustering_techniques: 'Clustering Techniques',
        federated_learning: 'Federated Learning',
    };

    const title = component.startsWith('report-') ? component.substring(7) : titles[component];

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
            <h1>Welcome to the Repository Catalog</h1>
            <p>Select a component from the sidebar to learn more about it.</p>
        </div>
    );
}

function ComponentViewer({ content }) {
    const htmlContent = marked.parse(content);
    return (
        <div className="component-container" dangerouslySetInnerHTML={{ __html: htmlContent }} />
    );
}

function ErrorMessage({ error }) {
    return <div className="error-message">{error}</div>;
}

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<App />);
