import React from 'react';
import PropTypes from 'prop-types';
import { PieChart } from '@mui/x-charts/PieChart';
import { BarChart, ScatterChart } from '@mui/x-charts';
import './Charts.css';
import Heatmap from '../Heatmap/Heatmap';

export default function Charts({data}){
  console.log(data)
  return (
    <div className="charts">
      <div className='piechart-container'>
        
        <div className='piechart' >
          <h2>Distribution of Reviews by Predicted Sentiment</h2>
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
        
        <div className='piechart' >
        <h2>Distribution of Reviews by Rating</h2>
          <PieChart 
            series={[{
                data: data.rating_counts,
                innerRadius: 20,
                outerRadius: 100,
                cx: 150,
                cy: 150,
              }
            ]}/>
        </div>
      </div>
        <div className='chart'>
        <h2>LSA of Review Texts</h2>
        <ScatterChart
          series={data.lsa_matrix}
          xAxis={[{
            label: "Component 1"
          }]}
          
          yAxis={[{
            label: "Component 2"
          }]}
        />
        </div>
        <br/><br/>
        <h2>Frequent Terms by VADER Classification</h2>
        <div className = 'frequent-terms-container'>
          <div className='frequent-terms'>
          <BarChart
            dataset={data.most_frequent_terms.positive}
            yAxis={[{ scaleType: 'band', dataKey: 'label' }]}
            series={[{ dataKey: 'count', label: 'Frequently Positive Terms'}]}
            layout="horizontal"
            />
          </div>
          <div className='frequent-terms'>
          <BarChart
            dataset={data.most_frequent_terms.neutral}
            yAxis={[{ scaleType: 'band', dataKey: 'label' }]}
            series={[{ dataKey: 'count', label: 'Frequently Neutral Terms'}]}
            layout="horizontal"
            />
          </div>
          <div className='frequent-terms'>
          <BarChart
            dataset={data.most_frequent_terms.negative}
            yAxis={[{ scaleType: 'band', dataKey: 'label' }]}
            series={[{ dataKey: 'count', label: 'Frequently Negative Terms'}]}
            layout="horizontal"
            />
          </div>
        </div>
        
        <h2>Frequent Terms by Rating</h2>
        <div className = 'frequent-terms-container'>
          <div className='frequent-terms'>
          <BarChart
            dataset={data.most_frequent_terms.one_two_three}
            yAxis={[{ scaleType: 'band', dataKey: 'label' }]}
            series={[{ dataKey: 'count', label: '1, 2, and 3 Star Reviews'}]}
            layout="horizontal"
            />
          </div>
          <div className='frequent-terms'>
          <BarChart
            dataset={data.most_frequent_terms.four}
            yAxis={[{ scaleType: 'band', dataKey: 'label' }]}
            series={[{ dataKey: 'count', label: '4 Star Reviews'}]}
            layout="horizontal"
            />
          </div>
          <div className='frequent-terms'>
          <BarChart
            dataset={data.most_frequent_terms.five}
            yAxis={[{ scaleType: 'band', dataKey: 'label' }]}
            series={[{ dataKey: 'count', label: '5 Star Reviews'}]}
            layout="horizontal"
            />
          </div>
        </div>
    </div>
  )
  
}
