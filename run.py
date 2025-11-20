#!/usr/bin/env python3
"""
Bot runner script
"""

if __name__ == "__main__":
    from bot.main import main
    import asyncio

    asyncio.run(main())
