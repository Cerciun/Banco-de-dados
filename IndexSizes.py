import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const data = [
  {
    name: 'Query 1',
    'Hash': 480,
    'B-tree': 520,
    'BRIN': 32,
    'Partial': 280,
    'Composite': 640
  },
  {
    name: 'Query 2',
    'Hash': 320,
    'B-tree': 360,
    'BRIN': 24,
    'Partial': 240,
    'Composite': 420
  },
  {
    name: 'Query 3',
    'Hash': 360,
    'B-tree': 400,
    'BRIN': 28,
    'Partial': 260,
    'Composite': 480
  },
  {
    name: 'Query 4',
    'Hash': 440,
    'B-tree': 480,
    'BRIN': 30,
    'Partial': 300,
    'Composite': 560
  },
  {
    name: 'Query 5',
    'Hash': 400,
    'B-tree': 440,
    'BRIN': 26,
    'Partial': 280,
    'Composite': 520
  }
];

const IndexSizes = () => {
  return (
    <div className="w-full max-w-6xl p-4">
      <h2 className="text-xl font-bold mb-4">Index Size Comparison</h2>
      <div className="h-96">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart
            data={data}
            margin={{ top: 20, right: 30, left: 20, bottom: 5 }}
          >
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="name" />
            <YAxis label={{ value: 'Size (KB)', angle: -90, position: 'insideLeft' }} />
            <Tooltip />
            <Legend />
            <Bar dataKey="Hash" fill="#82ca9d" />
            <Bar dataKey="B-tree" fill="#8884d8" />
            <Bar dataKey="BRIN" fill="#ffc658" />
            <Bar dataKey="Partial" fill="#ff8042" />
            <Bar dataKey="Composite" fill="#a4de6c" />
          </BarChart>
        </ResponsiveContainer>
      </div>
      <div className="mt-4 text-sm">
        <p className="font-semibold">Análise dos Resultados:</p>
        <ul className="list-disc pl-5 mt-2">
          <li>BRIN apresenta menor consumo de espaço em todas as consultas (24-32KB)</li>
          <li>Índices compostos são os mais pesados (420-640KB)</li>
          <li>Hash e B-tree têm tamanhos similares (320-520KB)</li>
          <li>Índices parciais são mais eficientes em espaço que os completos</li>
          <li>Consulta 1 gerou os maiores índices devido à complexidade das junções</li>
        </ul>
      </div>
    </div>
  );
};

export default IndexSizes;