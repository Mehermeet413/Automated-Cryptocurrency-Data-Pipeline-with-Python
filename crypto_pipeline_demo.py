#!/usr/bin/env python3
"""
Automated Cryptocurrency Data Pipeline with Python
Demo script for fetching, processing, and visualizing cryptocurrency data
"""

import pandas as pd
import numpy as np
import requests
import json
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import time
import os
from pathlib import Path

# Configuration
BASE_URL = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
# Note: For demo purposes, we'll use a sandbox URL if the API key doesn't work
SANDBOX_URL = 'https://sandbox-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'

class CryptoPipeline:
    def __init__(self, api_key=None, use_sandbox=False):
        """
        Initialize the cryptocurrency data pipeline
        
        Args:
            api_key (str): CoinMarketCap API key
            use_sandbox (bool): Whether to use sandbox environment
        """
        self.api_key = api_key or "ad7a73ca-faa9-4449-8c96-d7a6e83feba1"  # Your actual API key
        self.base_url = SANDBOX_URL if use_sandbox else BASE_URL
        self.df = pd.DataFrame()
        self.session = requests.Session()
        
        # Set up headers
        self.headers = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': self.api_key,
        }
        self.session.headers.update(self.headers)
        
        # Set pandas display options
        pd.set_option('display.max_columns', None)
        pd.set_option('display.max_rows', None)
        pd.set_option('display.float_format', lambda x: '%.5f' % x)
    
    def fetch_crypto_data(self, start=1, limit=15, convert='USD'):
        """
        Fetch cryptocurrency data from API
        
        Args:
            start (int): Starting rank
            limit (int): Number of cryptocurrencies to fetch
            convert (str): Currency to convert prices to
            
        Returns:
            dict: API response data or None if error
        """
        parameters = {
            'start': str(start),
            'limit': str(limit),
            'convert': convert
        }
        
        try:
            response = self.session.get(self.base_url, params=parameters)
            response.raise_for_status()
            data = response.json()
            return data
        except requests.exceptions.RequestException as e:
            print(f"API request failed: {e}")
            # Return mock data for demonstration
            return self._get_mock_data()
        except json.JSONDecodeError as e:
            print(f"Failed to parse JSON response: {e}")
            return self._get_mock_data()
    
    def _get_mock_data(self):
        """Generate mock data for demonstration purposes"""
        mock_data = {
            'data': [
                {
                    'id': 1,
                    'name': 'Bitcoin',
                    'symbol': 'BTC',
                    'slug': 'bitcoin',
                    'cmc_rank': 1,
                    'quote': {
                        'USD': {
                            'price': 45000.50 + np.random.normal(0, 1000),
                            'percent_change_1h': np.random.normal(0, 2),
                            'percent_change_24h': np.random.normal(0, 5),
                            'percent_change_7d': np.random.normal(0, 10),
                            'percent_change_30d': np.random.normal(0, 15),
                            'percent_change_60d': np.random.normal(0, 20),
                            'percent_change_90d': np.random.normal(0, 25),
                            'market_cap': 800000000000,
                            'volume_24h': 25000000000
                        }
                    }
                },
                {
                    'id': 2,
                    'name': 'Ethereum',
                    'symbol': 'ETH',
                    'slug': 'ethereum',
                    'cmc_rank': 2,
                    'quote': {
                        'USD': {
                            'price': 3200.75 + np.random.normal(0, 200),
                            'percent_change_1h': np.random.normal(0, 2),
                            'percent_change_24h': np.random.normal(0, 5),
                            'percent_change_7d': np.random.normal(0, 10),
                            'percent_change_30d': np.random.normal(0, 15),
                            'percent_change_60d': np.random.normal(0, 20),
                            'percent_change_90d': np.random.normal(0, 25),
                            'market_cap': 400000000000,
                            'volume_24h': 15000000000
                        }
                    }
                },
                {
                    'id': 3,
                    'name': 'Tether',
                    'symbol': 'USDT',
                    'slug': 'tether',
                    'cmc_rank': 3,
                    'quote': {
                        'USD': {
                            'price': 1.00 + np.random.normal(0, 0.01),
                            'percent_change_1h': np.random.normal(0, 0.1),
                            'percent_change_24h': np.random.normal(0, 0.2),
                            'percent_change_7d': np.random.normal(0, 0.3),
                            'percent_change_30d': np.random.normal(0, 0.5),
                            'percent_change_60d': np.random.normal(0, 0.7),
                            'percent_change_90d': np.random.normal(0, 1.0),
                            'market_cap': 90000000000,
                            'volume_24h': 50000000000
                        }
                    }
                }
            ]
        }
        return mock_data
    
    def process_data(self, data):
        """
        Process raw API data into a pandas DataFrame
        
        Args:
            data (dict): Raw API response data
            
        Returns:
            pd.DataFrame: Processed cryptocurrency data
        """
        if not data or 'data' not in data:
            return pd.DataFrame()
        
        # Normalize the JSON data
        df_new = pd.json_normalize(data['data'])
        
        # Add timestamp
        df_new['timestamp'] = pd.to_datetime('now')
        
        return df_new
    
    def append_data(self, new_data):
        """
        Append new data to the existing dataset
        
        Args:
            new_data (pd.DataFrame): New cryptocurrency data
        """
        if new_data.empty:
            return
        
        if self.df.empty:
            self.df = new_data.copy()
        else:
            # Use concat instead of deprecated append
            self.df = pd.concat([self.df, new_data], ignore_index=True)
    
    def run_data_collection(self, iterations=5, sleep_interval=10):
        """
        Run automated data collection
        
        Args:
            iterations (int): Number of data collection iterations
            sleep_interval (int): Sleep time between iterations (seconds)
        """
        print(f"Starting automated data collection for {iterations} iterations...")
        
        for i in range(iterations):
            print(f"Iteration {i+1}/{iterations}")
            
            # Fetch data
            raw_data = self.fetch_crypto_data()
            
            if raw_data:
                # Process data
                processed_data = self.process_data(raw_data)
                
                # Append to dataset
                self.append_data(processed_data)
                
                print(f"  - Collected data for {len(processed_data)} cryptocurrencies")
                print(f"  - Total dataset size: {len(self.df)} records")
            else:
                print("  - Failed to collect data")
            
            if i < iterations - 1:  # Don't sleep after the last iteration
                print(f"  - Sleeping for {sleep_interval} seconds...")
                time.sleep(sleep_interval)
        
        print("Data collection completed!")
    
    def save_to_csv(self, filename='crypto_data.csv'):
        """
        Save data to CSV file
        
        Args:
            filename (str): Output filename
        """
        if self.df.empty:
            print("No data to save")
            return
        
        filepath = Path(filename)
        self.df.to_csv(filepath, index=False)
        print(f"Data saved to {filepath.absolute()}")
    
    def load_from_csv(self, filename='crypto_data.csv'):
        """
        Load data from CSV file
        
        Args:
            filename (str): Input filename
        """
        filepath = Path(filename)
        if filepath.exists():
            self.df = pd.read_csv(filepath)
            self.df['timestamp'] = pd.to_datetime(self.df['timestamp'])
            print(f"Data loaded from {filepath.absolute()}")
            print(f"Dataset shape: {self.df.shape}")
        else:
            print(f"File {filepath.absolute()} not found")
    
    def analyze_price_trends(self):
        """
        Analyze cryptocurrency price trends over time
        
        Returns:
            pd.DataFrame: Aggregated trend analysis
        """
        if self.df.empty:
            print("No data available for analysis")
            return pd.DataFrame()
        
        # Calculate mean percentage changes by cryptocurrency
        trend_columns = [
            'quote.USD.percent_change_1h',
            'quote.USD.percent_change_24h', 
            'quote.USD.percent_change_7d',
            'quote.USD.percent_change_30d',
            'quote.USD.percent_change_60d',
            'quote.USD.percent_change_90d'
        ]
        
        available_columns = [col for col in trend_columns if col in self.df.columns]
        
        if not available_columns:
            print("No trend data available")
            return pd.DataFrame()
        
        trend_analysis = self.df.groupby('name', sort=False)[available_columns].mean()
        
        return trend_analysis
    
    def visualize_trends(self, save_plot=False):
        """
        Create visualizations of cryptocurrency trends
        
        Args:
            save_plot (bool): Whether to save the plot to file
        """
        if self.df.empty:
            print("No data available for visualization")
            return
        
        # Prepare data for visualization
        trend_data = self.analyze_price_trends()
        
        if trend_data.empty:
            print("No trend data available for visualization")
            return
        
        # Reshape data for visualization
        trend_melted = trend_data.reset_index().melt(
            id_vars=['name'], 
            var_name='time_period', 
            value_name='percent_change'
        )
        
        # Clean up time period labels
        trend_melted['time_period'] = trend_melted['time_period'].str.replace(
            'quote.USD.percent_change_', ''
        )
        
        # Create the plot
        plt.figure(figsize=(12, 8))
        sns.set_theme(style="whitegrid")
        
        # Line plot showing trends
        sns.lineplot(
            data=trend_melted, 
            x='time_period', 
            y='percent_change', 
            hue='name',
            marker='o'
        )
        
        plt.title('Cryptocurrency Price Change Trends Over Time')
        plt.xlabel('Time Period')
        plt.ylabel('Average Percent Change (%)')
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        if save_plot:
            plt.savefig('crypto_trends.png', dpi=300, bbox_inches='tight')
            print("Plot saved as 'crypto_trends.png'")
        
        plt.show()
    
    def visualize_bitcoin_price(self, save_plot=False):
        """
        Visualize Bitcoin price over time
        
        Args:
            save_plot (bool): Whether to save the plot to file
        """
        if self.df.empty:
            print("No data available for visualization")
            return
        
        # Filter for Bitcoin data
        bitcoin_data = self.df[self.df['name'] == 'Bitcoin'].copy()
        
        if bitcoin_data.empty:
            print("No Bitcoin data available")
            return
        
        # Create price timeline plot
        plt.figure(figsize=(12, 6))
        sns.set_theme(style="darkgrid")
        
        sns.lineplot(
            data=bitcoin_data, 
            x='timestamp', 
            y='quote.USD.price',
            linewidth=2,
            color='orange'
        )
        
        plt.title('Bitcoin Price Over Time', fontsize=16, fontweight='bold')
        plt.xlabel('Timestamp')
        plt.ylabel('Price (USD)')
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        if save_plot:
            plt.savefig('bitcoin_price.png', dpi=300, bbox_inches='tight')
            print("Plot saved as 'bitcoin_price.png'")
        
        plt.show()
    
    def get_summary_stats(self):
        """
        Get summary statistics of the dataset
        
        Returns:
            dict: Summary statistics
        """
        if self.df.empty:
            return {"message": "No data available"}
        
        stats = {
            "total_records": len(self.df),
            "unique_cryptocurrencies": self.df['name'].nunique() if 'name' in self.df.columns else 0,
            "data_collection_period": {
                "start": self.df['timestamp'].min().strftime('%Y-%m-%d %H:%M:%S') if 'timestamp' in self.df.columns else "N/A",
                "end": self.df['timestamp'].max().strftime('%Y-%m-%d %H:%M:%S') if 'timestamp' in self.df.columns else "N/A"
            },
            "top_cryptocurrencies": self.df['name'].value_counts().head().to_dict() if 'name' in self.df.columns else {}
        }
        
        return stats


def main():
    """
    Main demonstration function
    """
    print("=" * 60)
    print("Automated Cryptocurrency Data Pipeline Demonstration")
    print("=" * 60)
    
    # Initialize the pipeline
    pipeline = CryptoPipeline(use_sandbox=False)
    
    print("\n1. Fetching initial cryptocurrency data...")
    # Collect some sample data
    pipeline.run_data_collection(iterations=3, sleep_interval=2)
    
    print("\n2. Dataset Overview:")
    stats = pipeline.get_summary_stats()
    for key, value in stats.items():
        print(f"   {key}: {value}")
    
    print("\n3. Sample data:")
    if not pipeline.df.empty:
        print(pipeline.df[['name', 'symbol', 'quote.USD.price', 'timestamp']].head(10))
    
    print("\n4. Analyzing price trends...")
    trend_analysis = pipeline.analyze_price_trends()
    if not trend_analysis.empty:
        print("Average percentage changes by cryptocurrency:")
        print(trend_analysis)
    
    print("\n5. Creating visualizations...")
    # Create trend visualization
    pipeline.visualize_trends(save_plot=True)
    
    # Create Bitcoin price visualization
    pipeline.visualize_bitcoin_price(save_plot=True)
    
    print("\n6. Saving data to CSV...")
    pipeline.save_to_csv('crypto_pipeline_demo_data.csv')
    
    print("\n" + "=" * 60)
    print("Demonstration completed successfully!")
    print("Generated files:")
    print("  - crypto_pipeline_demo_data.csv (dataset)")
    print("  - crypto_trends.png (trend analysis plot)")
    print("  - bitcoin_price.png (Bitcoin price plot)")
    print("=" * 60)


if __name__ == "__main__":
    main()
