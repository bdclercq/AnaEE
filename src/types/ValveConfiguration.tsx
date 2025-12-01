//
//  ValveConfiguration.tsx
//  
//
//  Created by Beau De Clercq on 10/07/2025.
//

export interface ValveConfiguration {
  timestamp: string;     // ISO timestamp
  status: string;        // sequence like "010101"
  configtype?: 0 | 1;    // 1=start, 0=end, undefined=neither
}
