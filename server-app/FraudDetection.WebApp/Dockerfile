FROM mcr.microsoft.com/dotnet/aspnet:7.0 AS base
WORKDIR /app
EXPOSE 80
EXPOSE 443

FROM mcr.microsoft.com/dotnet/sdk:7.0 AS build
WORKDIR /src
COPY ["FraudDetection.BLL/FraudDetection.BLL.csproj", "FraudDetection.BLL/"]
COPY ["FraudDetection.DAL/FraudDetection.DAL.csproj", "FraudDetection.DAL/"]
COPY ["FraudDetection.WebApp/FraudDetection.WebApp.csproj", "FraudDetection.WebApp/"]
RUN dotnet restore "FraudDetection.WebApp/FraudDetection.WebApp.csproj"

COPY . .
WORKDIR "/src/FraudDetection.WebApp"
RUN dotnet build "FraudDetection.WebApp.csproj" -c Release -o /app/build

FROM build AS publish
RUN dotnet publish "FraudDetection.WebApp.csproj" -c Release -o /app/publish

FROM base AS final
WORKDIR /app
COPY --from=publish /app/publish .
ENTRYPOINT ["dotnet", "FraudDetection.WebApp.dll"]