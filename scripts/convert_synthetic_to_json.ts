import * as fs from 'fs';
import * as path from 'path';

const SOURCE_DIR = 'foundational_dataset_synthetic';
const DEST_DIR = 'frontend/public/data';

if (!fs.existsSync(DEST_DIR)) {
    fs.mkdirSync(DEST_DIR, { recursive: true });
}

const parseValue = (val: string) => {
    // Remove quotes if present
    if (val.startsWith('"') && val.endsWith('"')) {
        val = val.slice(1, -1);
    }
    // Try parse number
    // careful with empty strings
    if (val === '') return val;

    if (!isNaN(Number(val))) {
        return Number(val);
    }
    return val;
};

const parseLine = (line: string, headers: string[]) => {
    let row: any = {};
    let currentVal = '';
    let insideQuotes = false;
    let colIndex = 0;

    for (let i = 0; i < line.length; i++) {
        const char = line[i];
        if (char === '"') {
            insideQuotes = !insideQuotes;
        } else if (char === ',' && !insideQuotes) {
            if (colIndex < headers.length) {
                row[headers[colIndex]] = parseValue(currentVal.trim());
            }
            colIndex++;
            currentVal = '';
        } else {
            currentVal += char;
        }
    }
    // Last value
    if (colIndex < headers.length) {
        row[headers[colIndex]] = parseValue(currentVal.trim());
    }
    return row;
};

const csvToJson = (filename: string) => {
    const filePath = path.join(SOURCE_DIR, filename);
    if (!fs.existsSync(filePath)) {
        console.warn(`File not found: ${filePath}`);
        return;
    }

    const fileContent = fs.readFileSync(filePath, 'utf-8');
    const lines = fileContent.split('\n');

    // Filter out comments and empty lines
    const validLines = lines.filter(line => line.trim() !== '' && !line.trim().startsWith('#'));

    if (validLines.length === 0) return;

    const headers = validLines[0].split(',').map(h => h.trim());
    const data = validLines.slice(1).map(line => parseLine(line, headers));

    const outputFilename = filename.replace('.csv', '.json');
    fs.writeFileSync(path.join(DEST_DIR, outputFilename), JSON.stringify(data, null, 2));
    console.log(`Converted ${filename} to ${outputFilename}`);
};

const files = [
    'market_data_1min.csv',
    'analyst_ratings.csv',
    'corporate_earnings.csv',
    'social_hourly_features.csv'
];

files.forEach(csvToJson);
