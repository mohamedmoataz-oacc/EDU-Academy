import React from 'react'
import { Link, useMatch, useResolvedPath } from 'react-router-dom'

export function CustomLink({ to, children,className, ...props }) {
    const resolvedPath = useResolvedPath(to)
    const isActive = useMatch({ path: resolvedPath.pathname, end: true })
  
    return (
      <a className={isActive ? "active" : ""}>
        <Link to={to} className = {className} {...props}>
          {children}
        </Link>
      </a>
    )
  }