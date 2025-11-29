import React from 'react';

export const Card: React.FC<{children: React.ReactNode, className?: string}> = ({ children, className }) => <div className={`bg-gray-800 rounded p-4 ${className}`}>{children}</div>;
export const CardHeader: React.FC<{children: React.ReactNode}> = ({ children }) => <div className="mb-2">{children}</div>;
export const CardTitle: React.FC<{children: React.ReactNode}> = ({ children }) => <h3 className="text-lg font-bold">{children}</h3>;
export const CardContent: React.FC<{children: React.ReactNode}> = ({ children }) => <div>{children}</div>;
