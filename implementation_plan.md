# Swagger Documentation Enhancement Plan

The goal is to provide a comprehensive, industry-standard Swagger UI for the Bus Booking API. FastAPI automatically generates Swagger docs at `/docs`, but the current documentation is bare-bones and lacks descriptions, metadata, and rich response information.

## Proposed Changes

### Configuration & Main App
I will enhance [app/main.py](file:///c:/Users/admin/neuai/bus_booking_project/app/main.py) by adding rich OpenAPI metadata to the FastAPI instance.

#### [MODIFY] [main.py](file:///c:/Users/admin/neuai/bus_booking_project/app/main.py)
- **FastAPI Instance**: Add `description`, `version`, `contactInfo`, `terms_of_service`, `license_info`, and `openapi_tags`.
- **Tags Metadata**: Define descriptions for the `Buses`, `Bookings`, and `Authentication` tags so they appear nicely in the Swagger UI.

### Routers & Endpoints
I will enrich the endpoint definitions in the routers with `summary`, `description`, `response_description`, and detailed docstrings to explain what each route does, what parameters it expects, and what it returns.

#### [MODIFY] [buses.py](file:///c:/Users/admin/neuai/bus_booking_project/app/routers/buses.py)
- Add descriptions to [get_buses](file:///c:/Users/admin/neuai/bus_booking_project/app/routers/buses.py#45-49), [search_buses](file:///c:/Users/admin/neuai/bus_booking_project/app/routers/buses.py#51-65), [add_bus](file:///c:/Users/admin/neuai/bus_booking_project/app/routers/buses.py#68-75), [delete_bus](file:///c:/Users/admin/neuai/bus_booking_project/app/routers/buses.py#77-85), and [update_bus](file:///c:/Users/admin/neuai/bus_booking_project/app/routers/buses.py#87-100).
- Specify response details (e.g. 404 for Bus not found).

#### [MODIFY] [bookings.py](file:///c:/Users/admin/neuai/bus_booking_project/app/routers/bookings.py)
- Add descriptions to [create_booking](file:///c:/Users/admin/neuai/bus_booking_project/app/routers/bookings.py#15-43), [get_all_bookings](file:///c:/Users/admin/neuai/bus_booking_project/app/routers/bookings.py#47-51), [get_my_bookings](file:///c:/Users/admin/neuai/bus_booking_project/app/routers/bookings.py#55-59), and [get_booked_seats](file:///c:/Users/admin/neuai/bus_booking_project/app/routers/bookings.py#63-68).

#### [MODIFY] [auth.py](file:///c:/Users/admin/neuai/bus_booking_project/app/routers/auth.py)
- Add descriptions to [create_user](file:///c:/Users/admin/neuai/bus_booking_project/app/routers/auth.py#73-94) (signup) and [login](file:///c:/Users/admin/neuai/bus_booking_project/app/routers/auth.py#99-120).

## Verification Plan

### Manual Verification
1. Run the FastAPI server locally (`uvicorn app.main:app --reload` or through your normal startup script).
2. Open a web browser and navigate to `http://127.0.0.1:8000/docs`.
3. Visually inspect the Swagger Documentation:
   - Check that the main title, description, and contact info are displayed at the top.
   - Expand the `Buses`, `Bookings`, and `Authentication` tags to ensure their descriptions are visible.
   - Click on individual endpoints to ensure they have descriptive summaries and clear parameter/response documentation.
