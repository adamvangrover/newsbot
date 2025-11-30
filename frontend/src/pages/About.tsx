import React from 'react';
import { Github, Mail } from 'lucide-react';

const About: React.FC = () => {
  return (
    <div className="max-w-3xl mx-auto py-12 space-y-8">
      <div className="text-center">
        <h1 className="text-4xl font-bold text-white mb-4">About NewsBot Nexus</h1>
        <p className="text-xl text-gray-400">
          Bridging the gap between financial theory and synthetic reality.
        </p>
      </div>

      <div className="bg-gray-900 border border-gray-800 rounded-xl p-8 space-y-6 text-gray-300 leading-relaxed">
        <p>
          <strong className="text-white">NewsBot Nexus</strong> is an experimental platform designed to explore the intersection of
          Natural Language Processing (NLP), Knowledge Graphs, and Financial Market Simulation.
        </p>
        <p>
          Traditional financial models often rely on historical data that may not account for "Black Swan" events or complex
          geopolitical cascades. By generating high-fidelity synthetic data, this project aims to create a training ground
          for AI agents to learn reasoning patterns in a safe, controlled environment.
        </p>

        <h3 className="text-xl font-bold text-white mt-8">Project Goals</h3>
        <ul className="list-disc list-inside space-y-2 ml-4">
            <li>Develop robust <strong>Small Language Models (SLMs)</strong> capable of financial reasoning.</li>
            <li>Simulate <strong>second and third-order effects</strong> of news events on supply chains.</li>
            <li>Demonstrate <strong>Federated Learning</strong> capabilities for privacy-preserving model training.</li>
        </ul>
      </div>

      <div className="grid md:grid-cols-2 gap-6">
          <a href="#" className="flex items-center justify-center p-4 bg-gray-900 border border-gray-800 rounded-lg hover:bg-gray-800 transition-colors">
              <Github className="mr-2 text-white" />
              <span className="text-gray-300">View Source Code</span>
          </a>
          <a href="#" className="flex items-center justify-center p-4 bg-gray-900 border border-gray-800 rounded-lg hover:bg-gray-800 transition-colors">
              <Mail className="mr-2 text-white" />
              <span className="text-gray-300">Contact Developer</span>
          </a>
      </div>

      <div className="text-center text-sm text-gray-500 pt-8 border-t border-gray-800">
          &copy; 2024 NewsBot Nexus Project. All rights reserved.
      </div>
    </div>
  );
};

export default About;
