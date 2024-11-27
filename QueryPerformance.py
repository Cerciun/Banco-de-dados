import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const data = [
  {
    name: 'Query 1',
    'No Index': 19.980,
    'Hash': 15.467,
    'B-tree': 20.056,
    'BRIN': 20.107,
    'Partial': 20.061,
    'Composite': 20.182,
  },
  {
    name: 'Query 2',
    'No Index': 1.746,
    'Hash': 1.659,
    'B-tree': 1.645,
    'BRIN': 1.654,
    'Partial': 1.649,
    'Composite': 1.660,
  },
  {
    name: 'Query 3',
    'No Index': 28.800,
    'Hash': 29.118,
    'B-tree': 29.304,
    'BRIN': 29.416,
    'Partial': 29.557,
    'Composite': 29.256,
  },
  {
    name: 'Query 4',
    'No Index': 36.890,
    'Hash': 36.886,
    'B-tree': 48.540,
    'BRIN': 48.458,
    'Partial': 48.711,
    'Composite': 48.592,
  },
  {
    name: 'Query 5',
    'No Index': 47.460,
    'Hash': 55.795,
    'B-tree': 52.636,
    'BRIN': 52.533,
    'Partial': 52.592,
    'Composite': 52.592,
  },
];

const QueryPerformance = () => {
  return (
    <div className="w-full max-w-6xl p-4">
      <h2 className="text-xl font-bold mb-4">Query Performance Comparison</h2>
      <div className="h-96">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart
            data={data}
            margin={{ top: 20, right: 30, left: 20, bottom: 5 }}
          >
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="name" />
            <YAxis label={{ value: 'Execution Time (ms)', angle: -90, position: 'insideLeft' }} />
            <Tooltip />
            <Legend />
            <Bar dataKey="No Index" fill="#8884d8" />
            <Bar dataKey="Hash" fill="#82ca9d" />
            <Bar dataKey="B-tree" fill="#ffc658" />
            <Bar dataKey="BRIN" fill="#ff8042" />
            <Bar dataKey="Partial" fill="#a4de6c" />
            <Bar dataKey="Composite" fill="#d88484" />
          </BarChart>
        </ResponsiveContainer>
      </div>
      <div className="mt-4 text-sm">
        <p className="font-semibold">Análise dos Resultados:</p>
        <ul className="list-disc pl-5 mt-2">
          <li>Query 1 mostrou melhoria significativa com índice Hash (-22.6%)</li>
          <li>Query 2 teve pequena melhoria com B-tree (-5.8%)</li>
          <li>Query 3 manteve performance similar ou levemente pior</li>
          <li>Query 4 manteve performance com Hash, piorou com outros índices</li>
          <li>Query 5 teve performance degradada com todos os índices (+10.9% com B-tree)</li>
        </ul>
      </div>
    </div>
  );
};

export default QueryPerformance;