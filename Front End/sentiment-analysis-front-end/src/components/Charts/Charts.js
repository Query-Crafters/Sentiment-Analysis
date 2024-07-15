import React from 'react';
import PropTypes from 'prop-types';
import { PieChart } from '@mui/x-charts/PieChart';
import { BarChart } from '@mui/x-charts';
import './Charts.css';

export default function Charts({data}){
  console.log(data)
  return (
    <div className="charts">
      <div className="vader">
        <div className='chart' >
          <PieChart 
            series={[{
                data: data.vader_sentiment_counts,
                innerRadius: 20,
                outerRadius: 100,
                cx: 150,
                cy: 150,
              }
            ]}/>
        </div>
        <div className='chart'>
        <BarChart
          dataset={data.most_frequent_terms.positive}
          yAxis={[{ scaleType: 'band', dataKey: 'label' }]}
          series={[{ dataKey: 'count', label: 'Most Frequent Terms in Positive Reviews'}]}
          layout="horizontal"
          />
        </div>
        <div className='chart'>
        <BarChart
          dataset={data.most_frequent_terms.neutral}
          yAxis={[{ scaleType: 'band', dataKey: 'label' }]}
          series={[{ dataKey: 'count', label: 'Most Frequent Terms in Neutral Reviews'}]}
          layout="horizontal"
          />
        </div>
        <div className='chart'>
        <BarChart
          dataset={data.most_frequent_terms.negative}
          yAxis={[{ scaleType: 'band', dataKey: 'label' }]}
          series={[{ dataKey: 'count', label: 'Most Frequent Terms in Negative Reviews'}]}
          layout="horizontal"
          />
        </div>
      </div>
    </div>
  )
  
}
