# Rhumba Project Requirements

## Project Goal
Optimize rhum production in a greenhouse powered by solar panels, with initial implementation in Corti, Corsica, incorporating the new constants and project structure.

## System Requirements

### Hardware
- Medium-sized greenhouse with a total surface area of 10,000 m², including:
  - 6,000 to 10,000 m² for cane cultivation
  - 3,000 m² for solar panels
  - 1,000 m² for local facilities
- Solar panel installation with a total power of 1MWc, divided into:
  - 500kWc on the greenhouse
  - 500kWc on the ground
- Environmental monitoring equipment for tracking production energy, water consumption, product quality, temperature, and humidity

### Software
- JavaScript-based optimization solver
- Data collection and analysis tools
- Modular architecture supporting:
  * Greenhouse climate control
  * Solar energy management
  * Rhum production tracking
  * Monitoring of production energy, water consumption, product quality, temperature, and humidity

## Functional Requirements

1. **Production Optimization**
   - Maximize rhum production efficiency with a target production of 150,000 L per year
   - Minimize energy consumption
   - Optimize use of solar panel-generated electricity with an autoconsumption target of 1 MWp

2. **Data Management**
   - Real-time environmental data collection
   - Historical production data analysis
   - Performance metrics tracking, including energy efficiency ratio, production volume per solar energy unit, and reduction in operational costs

3. **Solar Energy Integration**
   - Monitor and manage solar panel energy output with an efficiency of 20% or more
   - Balance energy consumption with production needs

## Non-Functional Requirements

- **Scalability**: Ability to adapt to different greenhouse sizes
- **Reliability**: Continuous operation with minimal downtime
- **Maintainability**: Modular design for easy updates and maintenance, with scheduled maintenance including:
  - Monthly cleaning
  - Quarterly inspection
  - Annual maintenance

## Constraints

- Location-specific requirements for Corsican climate
- Compliance with local agricultural and energy regulations
- Budget limitations for initial prototype
- Tarification considerations

## Future Expansion Considerations

- Multi-site deployment
- Advanced machine learning for predictive optimization
- Potential for international greenhouse implementations

## Performance Metrics

- Energy efficiency ratio
- Production volume per solar energy unit
- Reduction in operational costs
- Production quality metrics, including cane yield, sugar content, extraction efficiency, and distillation efficiency

## Documentation

- [Documentation Technique](docs/technical.md)
- [Guide d'Utilisation](docs/user_guide.md)
- [Site officiel](https://github.com/JeanHuguesRobert/Rhuma)

## Contact

Pour toute question, contactez-nous à : institutmariani@gmail.com
