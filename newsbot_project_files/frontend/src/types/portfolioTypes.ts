export interface PortfolioAssetData {
    id: number;
    asset_id: number;
    portfolio_id: number;
    added_at: string;
}

export interface PortfolioData {
    id: number;
    user_id: number;
    name: string;
    description?: string | null;
    assets: PortfolioAssetData[];
    created_at: string;
    updated_at: string;
}
