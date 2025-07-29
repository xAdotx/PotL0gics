/// <reference types="vite/client" />

// Removed custom 'declare module "react"' to fix import errors

declare module 'react/jsx-runtime' {
  export default {}
  export const jsx: any
  export const jsxs: any
  export const Fragment: any
}

declare module 'react-router-dom' {
  import { ComponentType, ReactNode } from 'react'
  
  export interface LinkProps {
    to: string
    className?: string
    onClick?: () => void
    children?: ReactNode
  }
  
  export const Link: ComponentType<LinkProps>
  export const useLocation: () => { pathname: string }
  export const BrowserRouter: ComponentType<{ children: ReactNode }>
  export const Routes: ComponentType<{ children: ReactNode }>
  export const Route: ComponentType<{ path: string; element: ReactNode }>
}

declare module 'lucide-react' {
  import { FC, SVGProps } from 'react'
  
  export interface IconProps extends SVGProps<SVGSVGElement> {
    size?: number | string
    strokeWidth?: number
  }
  
  export const Home: FC<IconProps>
  export const Calculator: FC<IconProps>
  export const Activity: FC<IconProps>
  export const BarChart3: FC<IconProps>
  export const History: FC<IconProps>
  export const Settings: FC<IconProps>
  export const Menu: FC<IconProps>
  export const X: FC<IconProps>
  export const TrendingUp: FC<IconProps>
  export const DollarSign: FC<IconProps>
  export const Play: FC<IconProps>
  export const AlertCircle: FC<IconProps>
  export const CheckCircle: FC<IconProps>
}

declare namespace JSX {
  interface IntrinsicElements {
    [elemName: string]: any
  }
} 