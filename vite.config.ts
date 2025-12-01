//
//  vite.config.ts
//  
//
//  Created by Beau De Clercq on 09/07/2025.
//

import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  base: "./",
})
